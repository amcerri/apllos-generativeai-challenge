"""
Chainlit application for Apllos Assistant.

This module provides a chat interface for interacting with the multi-agent
assistant system through LangGraph Server.

Design
------
- Uses Chainlit for the chat UI
- Integrates with LangGraph Server via HTTP API
- Supports file attachments for commerce agent
- Displays formatted responses with citations and metadata
- Manages conversation threads for context persistence

Integration
-----------
- Connects to LangGraph Server at LANGGRAPH_SERVER_URL (default: http://localhost:2024)
- Uses threads for conversation context
- Handles async operations for query processing
"""

from __future__ import annotations

import asyncio
import os
import base64
from pathlib import Path
from typing import Any

import chainlit as cl
import httpx

from frontend.client import LangGraphClient
from frontend.utils import format_answer, format_error, format_metadata
from frontend.config import (
    LANGGRAPH_SERVER_URL,
    POLLING_INTERVAL_SECONDS,
    POLLING_TIMEOUT_SECONDS,
    UI_NAME,
)

# Disable Chainlit data layer by unsetting DATABASE_URL if it uses postgresql+psycopg://
# Chainlit's asyncpg doesn't support this format, and we don't need it anyway
# We use LangGraph Server for persistence, not Chainlit's data layer
_original_db_url = os.getenv("DATABASE_URL", "")
if _original_db_url.startswith("postgresql+psycopg://"):
    # Remove DATABASE_URL to disable Chainlit's data layer
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]
    if "CHAINLIT_DATABASE_URL" in os.environ:
        del os.environ["CHAINLIT_DATABASE_URL"]

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

POLLING_INTERVAL = POLLING_INTERVAL_SECONDS
POLLING_TIMEOUT = POLLING_TIMEOUT_SECONDS

# ---------------------------------------------------------------------------
# Chainlit Setup
# ---------------------------------------------------------------------------


@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialize chat session and create LangGraph thread."""
    # Initialize client
    client = LangGraphClient(base_url=LANGGRAPH_SERVER_URL)
    cl.user_session.set("client", client)
    
    # Create thread
    try:
        thread_id = await client.create_thread()
        cl.user_session.set("thread_id", thread_id)
        
        # Send welcome message
        welcome_msg = welcome_msg = (
            f"Olá! 👋 Sou o **{UI_NAME}**, seu assistente virtual para **análises, consultas e processamento de documentos**.\n\n"
            
            "Posso:\n"
            "- Consultar informações em **bancos de dados**\n"
            "- Buscar respostas em **bases de conhecimento**\n"
            "- **Extrair e analisar** dados de arquivos PDF, DOCX ou TXT\n\n"
            
            "Exemplos:\n"
            "- Quantos pedidos temos hoje?\n"
            "- O que significa _back office_ no e-commerce?\n"
            "- Extraia informações desse pedido ou fatura (anexe um PDF ou DOCX)\n\n"
            
            "Como posso ajudar hoje?"
        )
        await cl.Message(content=welcome_msg, author="Assistant").send()
    except Exception as e:
        error_msg = format_error(
            "Erro ao inicializar sessão",
            f"Não foi possível conectar ao servidor: {str(e)}",
        )
        await cl.Message(content=error_msg, author="Assistant").send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Process user message and send to LangGraph assistant."""
    client: LangGraphClient = cl.user_session.get("client")
    thread_id: str = cl.user_session.get("thread_id")
    
    if not client or not thread_id:
        await cl.Message(
            content=format_error(
                "Erro de sessão",
                "Sessão não inicializada. Por favor, recarregue a página.",
            ),
            author="Assistant",
        ).send()
        return
    
    # Prepare input
    input_data: dict[str, Any] = {}
    
    if message.content:
        input_data["query"] = message.content.strip()
    
    # Handle file attachments
    if message.elements:
        for element in message.elements:
            if hasattr(element, "path") and element.path:
                try:
                    # Read file
                    file_path = Path(element.path)
                    file_ext = file_path.suffix.lower()
                    is_binary = file_ext in {
                        ".pdf",
                        ".docx",
                        ".doc",
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".tiff",
                        ".bmp",
                    }
                    
                    if is_binary:
                        # Read as binary and base64 encode
                        with open(file_path, "rb") as f:
                            content_bytes = f.read()
                        content = base64.b64encode(content_bytes).decode("utf-8")
                        
                        # Determine MIME type
                        mime_types = {
                            ".pdf": "application/pdf",
                            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            ".doc": "application/msword",
                            ".png": "image/png",
                            ".jpg": "image/jpeg",
                            ".jpeg": "image/jpeg",
                            ".tiff": "image/tiff",
                            ".bmp": "image/bmp",
                        }
                        mime_type = mime_types.get(file_ext, "application/octet-stream")
                    else:
                        # Read as text
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        mime_type = "text/plain"
                    
                    input_data["attachment"] = {
                        "filename": file_path.name,
                        "content": content,
                        "mime_type": mime_type,
                    }
                    
                    # Show file info (no emojis)
                    await cl.Message(
                        content=f"Arquivo anexado: **{file_path.name}** ({mime_type})",
                        author="System",
                    ).send()
                except Exception as e:
                    await cl.Message(
                        content=format_error(
                            "Erro ao processar arquivo",
                            f"Não foi possível ler o arquivo: {str(e)}",
                        ),
                        author="Assistant",
                    ).send()
                    return
    
    if not input_data:
        await cl.Message(
            content=format_error(
                "Entrada inválida",
                "Por favor, forneça uma pergunta ou anexe um arquivo.",
            ),
            author="Assistant",
        ).send()
        return
    
    # Show processing indicator
    msg = cl.Message(content="Processando...", author="Assistant")
    await msg.send()
    
    # Process query
    try:
        # Create run
        run_id = await client.create_run(thread_id, input_data)
        
        # Poll for completion (no progress callback - just wait)
        result = await client.poll_for_answer(
            thread_id,
            run_id,
            polling_interval=POLLING_INTERVAL,
            polling_timeout=POLLING_TIMEOUT,
            progress_callback=None,  # No progress updates
        )
        
        if "error" in result:
            error_content = format_error("Erro", result["error"])
            # Replace processing message with error
            msg.content = error_content
            await msg.update()
            return
        
        # Format and display answer - ONLY the text, nothing else
        answer_text = format_answer(result)
        if not answer_text or answer_text.strip() == "Nenhuma resposta disponível.":
            # If no answer, try to get text from state directly
            state = await client.get_thread_state(thread_id)
            values = state.get("values", {})
            answer = values.get("answer")
            if isinstance(answer, dict):
                answer_text = answer.get("text", "Nenhuma resposta disponível.")
            elif answer:
                answer_text = str(answer)
        
        # Replace processing message with answer only (no metadata, citations, or followups)
        msg.content = answer_text
        await msg.update()
            
    except httpx.TimeoutException:
        error_content = format_error(
            "Timeout",
            "A requisição demorou muito para processar. Tente novamente.",
        )
        msg.content = error_content
        await msg.update()
    except httpx.HTTPStatusError as e:
        error_content = format_error(
            "Erro HTTP",
            f"Erro do servidor: {e.response.status_code} - {e.response.text}",
        )
        msg.content = error_content
        await msg.update()
    except Exception as e:
        error_content = format_error(
            "Erro inesperado",
            f"Ocorreu um erro: {str(e)}",
        )
        msg.content = error_content
        await msg.update()


@cl.on_stop
async def on_stop() -> None:
    """Handle session stop."""
    # Cleanup if needed
    pass
