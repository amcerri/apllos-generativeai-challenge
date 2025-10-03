#!/usr/bin/env python3
"""
Query Assistant - Interface de linha de comando para o assistente LangGraph.

Este script permite fazer perguntas e enviar attachments para o assistente,
deixando o router decidir qual agente usar (analytics, knowledge, commerce, triage).

Usage:
    python scripts/query_assistant.py --query "Como iniciar um e-commerce?"
    python scripts/query_assistant.py --query "Quantos pedidos temos?" --attachment "data/samples/invoice.pdf"
    python scripts/query_assistant.py --attachment "data/samples/order.txt"
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import httpx


class QueryAssistant:
    """Interface para consultar o assistente LangGraph."""
    
    def __init__(self, base_url: str = "http://localhost:2024"):
        self.base_url = base_url
        self.http_client = httpx.AsyncClient(timeout=60.0)
    
    async def query(
        self, 
        query: Optional[str] = None, 
        attachment_path: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fazer uma consulta ao assistente."""
        
        # Preparar input
        input_data = {}
        
        if query:
            input_data["query"] = query
        
        # Processar attachment apenas se fornecido
        if attachment_path:
            # Verificar se o arquivo existe
            if not os.path.exists(attachment_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {attachment_path}")
            
            # Determinar se é arquivo binário baseado na extensão
            file_ext = Path(attachment_path).suffix.lower()
            is_binary = file_ext in {'.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
            
            if is_binary:
                # Ler como binário e codificar em base64 para JSON
                import base64
                with open(attachment_path, 'rb') as f:
                    content_bytes = f.read()
                content = base64.b64encode(content_bytes).decode('utf-8')
                
                # Determinar MIME type baseado na extensão
                mime_types = {
                    '.pdf': 'application/pdf',
                    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    '.doc': 'application/msword',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.tiff': 'image/tiff',
                    '.bmp': 'image/bmp'
                }
                mime_type = mime_types.get(file_ext, 'application/octet-stream')
            else:
                # Ler como texto
                with open(attachment_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                mime_type = 'text/plain'
            
            input_data["attachment"] = {
                "filename": Path(attachment_path).name,
                "content": content,
                "mime_type": mime_type
            }
        elif thread_id and not attachment_path:
            # Se estamos reusing o thread mas não temos attachment novo, não envie attachment
            # (deixa o campo ausente do input_data para não sobrescrever o contexto)
            pass
        
        if not input_data:
            raise ValueError("Deve fornecer pelo menos uma query ou attachment")
        
        # Usar thread existente ou criar novo
        if thread_id:
            # Verificar se o thread existe
            try:
                response = await self.http_client.get(f"{self.base_url}/threads/{thread_id}")
                response.raise_for_status()
                print(f"🔄 Reutilizando thread: {thread_id}")
            except Exception:
                print(f"⚠️ Thread {thread_id} não encontrado, criando novo...")
                thread_id = None
        
        if not thread_id:
            # Criar novo thread
            response = await self.http_client.post(f"{self.base_url}/threads", json={})
            response.raise_for_status()
            thread_data = response.json()
            thread_id = thread_data["thread_id"]
            # Salvar thread_id para próxima execução (apenas para referência)
            with open(".last_thread_id", "w") as f:
                f.write(thread_id)
        
        print(f"🔗 Thread ID: {thread_id}")
        print(f"📝 Input: {json.dumps(input_data, indent=2, ensure_ascii=False)}")
        print("⏳ Processando...")
        
        # Executar run
        run_data = {
            "assistant_id": "assistant",
            "input": input_data
        }
        
        response = await self.http_client.post(
            f"{self.base_url}/threads/{thread_id}/runs",
            json=run_data
        )
        response.raise_for_status()
        run_data = response.json()
        run_id = run_data["run_id"]
        
        # Aguardar conclusão
        max_attempts = 30  # 30 tentativas de 1 segundo
        for attempt in range(max_attempts):
            response = await self.http_client.get(f"{self.base_url}/threads/{thread_id}/state")
            response.raise_for_status()
            state = response.json()
            
            values = state.get("values", {})
            if values.get("answer"):
                break
            
            # Debug: mostrar estado a cada 5 segundos
            if attempt % 5 == 0:
                print(f"⏳ Aguardando... ({attempt + 1}s)")
                # Mostrar informações de debug
                tasks = state.get("tasks", [])
                agent = values.get("agent", "N/A")
                print(f"🔍 Debug - Agente: {agent}, Tarefas: {len(tasks)}")
            
            await asyncio.sleep(1)
        else:
            print("❌ Timeout: A consulta demorou muito para ser processada")
            return {"error": "timeout"}
        
        # Extrair resposta
        answer = values.get("answer", {})
        if isinstance(answer, dict):
            text = answer.get("text", "Nenhuma resposta encontrada")
            citations = answer.get("citations", [])
            meta = answer.get("meta", {})
        else:
            text = str(answer) if answer else "Nenhuma resposta encontrada"
            citations = []
            meta = {}
        
        # Mostrar informações do roteamento
        router_decision = values.get("router_decision", {})
        agent = values.get("agent", "unknown")
        
        print(f"\nAgent: {agent}")
        if router_decision:
            print(f"Confidence: {router_decision.get('confidence', 'N/A')}")
            print(f"Reason: {router_decision.get('reason', 'N/A')}")
        
        # Show response
        print(f"\nResponse:")
        print("=" * 60)
        print(text)
        print("=" * 60)
        
        # Show citations if available
        if citations:
            print(f"\nCitations ({len(citations)}):")
            for i, citation in enumerate(citations, 1):
                title = citation.get('title', 'No title')
                print(f"  {i}. {title}")
        
        # Show chunks if available
        chunks = answer.get('chunks', [])
        if chunks:
            print(f"\nDocument Chunks ({len(chunks)}):")
            for i, chunk in enumerate(chunks, 1):
                title = chunk.get('title', f'Chunk {i}')
                content = chunk.get('content', 'No content')
                # Truncate for console display
                if len(content) > 200:
                    content = content[:200] + "..."
                print(f"  {i}. {title}")
                print(f"     {content}")
                print()
        
        # Show metadata
        if meta:
            print(f"\nMetadata:")
            for key, value in meta.items():
                print(f"  {key}: {value}")
        
        return {
            "thread_id": thread_id,
            "agent": agent,
            "answer": text,
            "citations": citations,
            "meta": meta,
            "router_decision": router_decision
        }
    
    async def close(self):
        """Fechar o cliente HTTP."""
        await self.http_client.aclose()


async def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Consultar o assistente LangGraph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/query_assistant.py --query "Como iniciar um e-commerce?"
  python scripts/query_assistant.py --query "Quantos pedidos temos?" --attachment "data/samples/invoice.pdf"
  python scripts/query_assistant.py --attachment "data/samples/order.txt"
        """
    )
    
    parser.add_argument(
        "--query", 
        type=str, 
        help="Pergunta para o assistente"
    )
    
    parser.add_argument(
        "--attachment", 
        type=str, 
        help="Caminho para arquivo anexo"
    )
    
    parser.add_argument(
        "--base-url", 
        type=str, 
        default="http://localhost:2024",
        help="URL base do LangGraph (padrão: http://localhost:2024)"
    )
    
    parser.add_argument(
        "--thread-id", 
        type=str, 
        help="ID do thread para reutilizar contexto existente"
    )
    
    args = parser.parse_args()
    
    if not args.query and not args.attachment:
        print("❌ Erro: Deve fornecer pelo menos --query ou --attachment")
        parser.print_help()
        sys.exit(1)
    
    # Verificar se o servidor está rodando
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{args.base_url}/ok")
            if response.status_code != 200:
                print(f"Server not responding at {args.base_url}")
                sys.exit(1)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        print(f"Make sure LangGraph Studio is running:")
        print(f"   make studio-up")
        sys.exit(1)
    
    # Executar consulta
    assistant = QueryAssistant(args.base_url)
    try:
        result = await assistant.query(args.query, args.attachment, args.thread_id)
        
        if "error" in result:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erro durante a consulta: {e}")
        sys.exit(1)
    finally:
        await assistant.close()


if __name__ == "__main__":
    asyncio.run(main())
