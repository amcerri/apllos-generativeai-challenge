#!/usr/bin/env python3
"""
Query Assistant - Command-line interface for the LangGraph assistant.

This script allows asking questions and sending attachments to the assistant,
letting the router decide which agent to use (analytics, knowledge, commerce, triage).

Usage:
    python scripts/query_assistant.py --query "How to start an e-commerce?"
    python scripts/query_assistant.py --query "How many orders do we have?" --attachment "data/samples/invoice.pdf"
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
    """Thin HTTP client to query the LangGraph assistant."""
    
    def __init__(self, base_url: str = "http://localhost:2024"):
        self.base_url = base_url
        
        # Load configuration
        try:
            from app.config.settings import get_settings
            settings = get_settings()
            http_timeout = float(settings.query_client.http_timeout_seconds)
            polling_timeout = settings.query_client.polling_timeout_seconds
            polling_interval = settings.query_client.polling_interval_seconds
        except Exception:
            # Fallback to defaults if config not available
            http_timeout = 300.0
            polling_timeout = 300
            polling_interval = 1
        
        self.http_client = httpx.AsyncClient(timeout=http_timeout)
        self.polling_timeout = polling_timeout
        self.polling_interval = polling_interval
    
    async def query(
        self,
        query: Optional[str] = None,
        attachment_path: Optional[str] = None,
        thread_id: Optional[str] = None,
        export: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send a query to the assistant and optionally export tabular data.

        Parameters
        ----------
        query: str | None
            Natural language question.
        attachment_path: str | None
            Local path to an attachment file.
        thread_id: str | None
            Existing thread id to reuse context.
        export: str | None
            Optional path to export results (CSV or Markdown by extension).
        """
        
        # Preparar input
        input_data = {}
        
        if query:
            input_data["query"] = query
        
        # Processar attachment apenas se fornecido
        if attachment_path:
            # Check file existence
            if not os.path.exists(attachment_path):
                raise FileNotFoundError(f"File not found: {attachment_path}")
            
            # Determinar se é arquivo binário baseado na extensão
            file_ext = Path(attachment_path).suffix.lower()
            is_binary = file_ext in {'.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
            
            if is_binary:
                # Read as binary and base64 encode for JSON
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
                # Read as text
                with open(attachment_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                mime_type = 'text/plain'
            
            input_data["attachment"] = {
                "filename": Path(attachment_path).name,
                "content": content,
                "mime_type": mime_type
            }
        elif thread_id and not attachment_path:
            # Reuse thread without overriding attachment
            pass
        
        if not input_data:
            raise ValueError("Deve fornecer pelo menos uma query ou attachment")
        
        # Usar thread existente ou criar novo
        if thread_id:
            # Check if thread exists
            try:
                response = await self.http_client.get(f"{self.base_url}/threads/{thread_id}")
                response.raise_for_status()
                print(f"🔄 Reusing thread: {thread_id}")
            except Exception:
                print(f"⚠️ Thread {thread_id} not found, creating a new one...")
                thread_id = None
        
        if not thread_id:
            # Criar novo thread
            response = await self.http_client.post(f"{self.base_url}/threads", json={})
            response.raise_for_status()
            thread_data = response.json()
            thread_id = thread_data["thread_id"]
        
        print(f"🔗 Thread ID: {thread_id}")
        print(f"📝 Input: {json.dumps(input_data, indent=2, ensure_ascii=False)}")
        print("⏳ Processing...")
        
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
        
        # Poll for completion
        max_attempts = self.polling_timeout // self.polling_interval
        for attempt in range(max_attempts):
            response = await self.http_client.get(f"{self.base_url}/threads/{thread_id}/state")
            response.raise_for_status()
            state = response.json()
            
            values = state.get("values", {})
            if values.get("answer"):
                break
            
            # Debug progress every 5 seconds
            if attempt % 5 == 0:
                elapsed = (attempt + 1) * self.polling_interval
                print(f"⏳ Waiting... ({elapsed}s)")
                tasks = state.get("tasks", [])
                agent = values.get("agent", "N/A")
                print(f"🔍 Debug - Agent: {agent}, Tasks: {len(tasks)}")
            
            await asyncio.sleep(self.polling_interval)
        else:
            print("❌ Timeout: processing took too long")
            return {"error": "timeout"}
        
        # Extrair resposta
        answer = values.get("answer", {})
        if isinstance(answer, dict):
            text = answer.get("text", "No answer found")
            citations = answer.get("citations", [])
            meta = answer.get("meta", {})
        else:
            text = str(answer) if answer else "No answer found"
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
        
        # Optional export
        if export:
            try:
                export_path = Path(export)
                if export_path.suffix.lower() == ".csv" and isinstance(meta.get("data"), list):
                    import csv
                    rows = meta.get("data") or []
                    cols = meta.get("columns") or []
                    with export_path.open("w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        if cols:
                            writer.writerow(cols)
                        for r in rows:
                            writer.writerow(r)
                    print(f"💾 Exported CSV to {export_path}")
                elif export_path.suffix.lower() in {".md", ".markdown"}:
                    with export_path.open("w", encoding="utf-8") as f:
                        f.write(f"# Assistant Response\n\n{text}\n")
                    print(f"💾 Exported Markdown to {export_path}")
            except Exception as exc:
                print(f"⚠️ Export failed: {exc}")

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
        description="Query the LangGraph assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/query_assistant.py --query "How to start an e-commerce?"
  python scripts/query_assistant.py --query "How many orders do we have?" --attachment "data/samples/invoice.pdf"
  python scripts/query_assistant.py --attachment "data/samples/order.txt"
        """
    )
    
    parser.add_argument(
        "--query", 
        type=str, 
        help="Question for the assistant"
    )
    
    parser.add_argument(
        "--attachment", 
        type=str, 
        help="Path to attachment file"
    )
    
    parser.add_argument(
        "--base-url", 
        type=str, 
        default="http://localhost:2024",
        help="Base URL for LangGraph (default: http://localhost:2024)"
    )
    
    parser.add_argument(
        "--thread-id", 
        type=str, 
        help="Thread ID to reuse existing context"
    )

    parser.add_argument(
        "--export",
        type=str,
        help="Optional export path (.csv or .md) for results"
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
        result = await assistant.query(args.query, args.attachment, args.thread_id, args.export)
        
        if "error" in result:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error during query: {e}")
        sys.exit(1)
    finally:
        await assistant.close()


if __name__ == "__main__":
    asyncio.run(main())
