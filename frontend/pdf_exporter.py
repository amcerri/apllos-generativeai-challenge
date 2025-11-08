"""
PDF exporter for conversation history.

Overview
  Generates PDF documents from conversation history for easy sharing and archiving.
  Uses reportlab for PDF generation with professional formatting.

Design
  - Extracts conversation history from LangGraph thread state
  - Formats messages with proper styling (user vs assistant)
  - Includes metadata (timestamp, agent, thread_id)
  - Professional layout with headers and sections

Integration
  - Used by Chainlit frontend to export conversations
  - Accesses conversation_history from GraphState via LangGraph client

Usage
  >>> from frontend.pdf_exporter import export_conversation_to_pdf
  >>> pdf_bytes = await export_conversation_to_pdf(thread_id, client)
  >>> # Use cl.File to provide download
"""

from __future__ import annotations

import io
from datetime import datetime
from typing import Any

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from app.infra.logging import get_logger
except Exception:
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

__all__ = ["export_conversation_to_pdf"]


async def export_conversation_to_pdf(
    thread_id: str,
    client: Any,
    title: str | None = None,
    include_metadata: bool = False,
) -> bytes | None:
    """Export conversation history to PDF.

    Parameters
    ----------
    thread_id
        LangGraph thread ID containing conversation history.
    client
        LangGraphClient instance for accessing thread state.
    title
        Optional custom title for the PDF document.
    include_metadata
        If True, includes metadata (SQL queries, chunks, citations, etc.) in the PDF.

    Returns
    -------
    bytes | None
        PDF file content as bytes, or None if export fails.
    """
    if not REPORTLAB_AVAILABLE:
        return None

    try:
        # Get thread state with conversation history
        state = await client.get_thread_state(thread_id)
        values = state.get("values", {})
        conversation_history = values.get("conversation_history", [])
        
        # Store full state for metadata extraction if needed
        full_state = state if include_metadata else None

        if not conversation_history:
            return None

        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Build PDF content
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=30,
            alignment=TA_LEFT,
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=12,
            spaceBefore=12,
        )

        user_style = ParagraphStyle(
            "UserMessage",
            parent=styles["BodyText"],
            fontSize=11,
            textColor=colors.HexColor("#2c3e50"),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12,
            spaceBefore=4,
            alignment=TA_LEFT,
            leading=14,
        )

        assistant_style = ParagraphStyle(
            "AssistantMessage",
            parent=styles["BodyText"],
            fontSize=11,
            textColor=colors.HexColor("#2c3e50"),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12,
            spaceBefore=4,
            alignment=TA_LEFT,
            leading=14,
        )

        metadata_style = ParagraphStyle(
            "Metadata",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#7f8c8d"),
            spaceAfter=20,
        )
        
        # Metadata section styles
        metadata_header_style = ParagraphStyle(
            "MetadataHeader",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#7f8c8d"),
            spaceAfter=4,
            spaceBefore=8,
            fontName="Helvetica-Bold",
        )
        
        metadata_content_style = ParagraphStyle(
            "MetadataContent",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#555555"),
            leftIndent=15,
            rightIndent=15,
            spaceAfter=6,
            backColor=colors.HexColor("#f5f5f5"),
            borderPadding=6,
        )
        
        sql_style = ParagraphStyle(
            "SQLStyle",
            parent=styles["Code"],
            fontSize=8,
            textColor=colors.HexColor("#8e44ad"),
            leftIndent=15,
            rightIndent=15,
            spaceAfter=6,
            fontName="Courier",
            backColor=colors.HexColor("#f9f9f9"),
            borderPadding=6,
        )

        # Title
        doc_title = title or "Histórico de Conversa"
        story.append(Paragraph(doc_title, title_style))
        story.append(Spacer(1, 0.2 * inch))

        # Metadata
        export_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        metadata_text = f"Thread ID: {thread_id} | Exportado em: {export_date}"
        story.append(Paragraph(metadata_text, metadata_style))
        story.append(Spacer(1, 0.3 * inch))

        # Process and deduplicate messages
        seen_messages = set()
        processed_messages = []
        
        for msg in conversation_history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "") or msg.get("text", "")
            timestamp = msg.get("timestamp")
            
            # Extract text from Answer object if content is a string representation
            content = _extract_text_from_content(content)
            
            if not content or not content.strip():
                continue
            
            # Create a unique key for deduplication
            msg_key = (role, content[:100], timestamp)
            if msg_key in seen_messages:
                continue
            seen_messages.add(msg_key)
            
            processed_messages.append({
                "role": role,
                "content": content,
                "timestamp": timestamp,
                "agent": msg.get("agent"),
            })
        
        # Conversation messages
        for i, msg in enumerate(processed_messages):
            role = msg["role"]
            content = msg["content"]
            timestamp = msg.get("timestamp")
            agent = msg.get("agent")

            # Format role label with better styling
            if role == "user":
                role_label = "👤 Usuário"
                role_color = colors.HexColor("#3498db")
            else:
                agent_display = agent if agent else "Assistente"
                agent_names = {
                    "analytics": "Analytics",
                    "knowledge": "Knowledge",
                    "commerce": "Commerce",
                    "triage": "Triage",
                }
                agent_display = agent_names.get(agent, agent_display)
                role_label = f"🤖 Assistente ({agent_display})"
                role_color = colors.HexColor("#2ecc71")

            # Format timestamp
            timestamp_str = ""
            if timestamp:
                try:
                    # Timestamp is Unix time (seconds since epoch)
                    from datetime import datetime as dt
                    dt_obj = dt.fromtimestamp(float(timestamp))
                    timestamp_str = dt_obj.strftime("%d/%m/%Y às %H:%M:%S")
                except (ValueError, TypeError, OSError):
                    # If timestamp is already formatted or invalid, use as-is
                    timestamp_str = str(timestamp)

            # Create message header style with color
            header_style = ParagraphStyle(
                "MessageHeader",
                parent=styles["Normal"],
                fontSize=12,
                textColor=role_color,
                spaceAfter=6,
                spaceBefore=12,
                fontName="Helvetica-Bold",
            )

            # Add message header
            header_text = role_label
            if timestamp_str:
                header_text += f" <font color='#7f8c8d' size='9'>{timestamp_str}</font>"
            story.append(Paragraph(header_text, header_style))

            # Add message content with better formatting
            content_cleaned = _clean_content(content)
            
            # If content is still very long and looks like object representation, try to extract just the text
            if len(content_cleaned) > 500 and ("Answer(" in content_cleaned or "text=" in content_cleaned):
                # Try one more time to extract just the text part
                extracted = _extract_text_from_content(content_cleaned)
                if extracted and extracted != content_cleaned:
                    content_cleaned = extracted
            
            content_escaped = _escape_html(content_cleaned)
            content_formatted = _format_markdown(content_escaped)

            style = user_style if role == "user" else assistant_style
            story.append(Paragraph(content_formatted, style))
            
            # Add metadata if requested and available
            if include_metadata and role == "assistant" and full_state:
                metadata_content = _extract_metadata_for_message(msg, full_state, i)
                if metadata_content:
                    story.append(Spacer(1, 0.1 * inch))
                    # metadata_content is a list of Paragraph objects
                    for para in metadata_content:
                        story.append(para)
            
            story.append(Spacer(1, 0.3 * inch))

            # Add page break every 8 messages to avoid very long pages
            if (i + 1) % 8 == 0:
                story.append(PageBreak())

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Failed to export conversation to PDF: {e}", exc_info=True)
        return None


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _extract_text_from_content(content: str) -> str:
    """Extract clean text from content, handling Answer object representations."""
    if not content:
        return ""
    
    # If content is already a simple string, return it
    if not isinstance(content, str):
        content = str(content)
    
    # If content looks like a Python object representation (Answer(...)), extract text field
    import re
    
    # Check if it's an Answer object representation
    if "Answer(text=" in content or ("text=" in content and ("Answer" in content or "data=" in content)):
        # Try to extract text field value with proper quote handling
        # Handle both single and double quotes, and multiline strings
        
        # First, try to find text='...' or text="..." with proper quote matching
        # This handles multiline strings better
        quote_patterns = [
            r"text='(.*?)'(?=\s*[,)])",  # text='...' followed by comma or closing paren
            r'text="(.*?)"(?=\s*[,)])',  # text="..." followed by comma or closing paren
        ]
        
        for pattern in quote_patterns:
            text_match = re.search(pattern, content, re.DOTALL)
            if text_match:
                text_value = text_match.group(1)
                # Handle escaped characters
                text_value = text_value.replace("\\'", "'").replace('\\"', '"')
                text_value = text_value.replace("\\n", "\n").replace("\\t", "\t")
                if text_value.strip():
                    return text_value
        
        # Fallback: try to extract text=... without quotes (less reliable)
        fallback_match = re.search(r"text=([^,)]+?)(?=\s*[,)])", content, re.DOTALL)
        if fallback_match:
            text_value = fallback_match.group(1).strip()
            text_value = text_value.strip("'\"")
            if text_value:
                return text_value
    
    return content


def _clean_content(text: str) -> str:
    """Clean content text for better display."""
    if not text:
        return ""
    
    # Remove common unwanted patterns
    import re
    
    # Remove Answer object representation patterns
    text = re.sub(r"Answer\([^)]+\)", "", text)
    
    # Remove extra whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    
    return text


def _format_markdown(text: str) -> str:
    """Convert basic markdown to HTML for PDF rendering."""
    import re

    # Bold: **text** -> <b>text</b>
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Italic: *text* -> <i>text</i> (but not if it's part of **text**)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    # Code: `text` -> <font face='Courier' color='#8e44ad'>text</font>
    text = re.sub(r"`(.+?)`", r"<font face='Courier' color='#8e44ad'>\1</font>", text)
    # Line breaks: \n -> <br/>
    text = text.replace("\n", "<br/>")
    # Remove multiple consecutive <br/> tags (max 2)
    text = re.sub(r"(<br/>){3,}", "<br/><br/>", text)
    return text


def _extract_metadata_for_message(
    msg: dict[str, Any],
    full_state: dict[str, Any],
    message_index: int,
) -> list[Any] | None:
    """Extract and format metadata for a message.
    
    Returns a list of Paragraph objects to add to the PDF story, or None if no metadata.
    """
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    
    styles = getSampleStyleSheet()
    metadata_parts = []
    
    # Get the answer from state
    values = full_state.get("values", {})
    last_answer = values.get("last_answer")
    
    # Try to match message with answer by checking conversation history
    conversation_history = values.get("conversation_history", [])
    
    # Get answer from state - we'll use the last_answer for now
    # In a more sophisticated implementation, we could match by timestamp
    answer = None
    if last_answer and isinstance(last_answer, dict):
        answer = last_answer
    
    # If we have an answer with metadata, format it
    if answer and isinstance(answer, dict):
        meta = answer.get("meta", {})
        sql = meta.get("sql")
        row_count = meta.get("row_count")
        citations = answer.get("citations")
        chunks = answer.get("chunks")
        followups = answer.get("followups")
        
        has_metadata = bool(sql or row_count is not None or citations or chunks or followups)
        
        if has_metadata:
            metadata_header_style = ParagraphStyle(
                "MetadataHeader",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#7f8c8d"),
                spaceAfter=4,
                spaceBefore=8,
                fontName="Helvetica-Bold",
            )
            
            metadata_content_style = ParagraphStyle(
                "MetadataContent",
                parent=styles["Normal"],
                fontSize=9,
                textColor=colors.HexColor("#555555"),
                leftIndent=15,
                rightIndent=15,
                spaceAfter=6,
            )
            
            sql_style = ParagraphStyle(
                "SQLStyle",
                parent=styles["Code"],
                fontSize=8,
                textColor=colors.HexColor("#8e44ad"),
                leftIndent=15,
                rightIndent=15,
                spaceAfter=6,
                fontName="Courier",
            )
            
            metadata_parts.append(Paragraph("<b>📊 Metadados:</b>", metadata_header_style))
            
            # SQL Query
            if sql:
                sql_escaped = _escape_html(sql)
                metadata_parts.append(Paragraph("<b>SQL:</b>", metadata_content_style))
                metadata_parts.append(Paragraph(f"<font face='Courier' color='#8e44ad'>{sql_escaped}</font>", sql_style))
            
            # Row count
            if row_count is not None:
                metadata_parts.append(Paragraph(f"<b>Linhas retornadas:</b> {row_count}", metadata_content_style))
            
            # Citations
            if citations:
                metadata_parts.append(Paragraph("<b>Referências:</b>", metadata_content_style))
                for i, citation in enumerate(citations[:5], 1):  # Limit to 5 citations
                    if isinstance(citation, dict):
                        title = citation.get("title", "Sem título")
                        doc_id = citation.get("doc_id")
                        url = citation.get("url")
                        ref_text = f"{i}. {title}"
                        if doc_id:
                            ref_text += f" (ID: {doc_id})"
                        if url:
                            ref_text += f" - {url}"
                        metadata_parts.append(Paragraph(f"  • {_escape_html(ref_text)}", metadata_content_style))
            
            # Chunks (document chunks)
            if chunks:
                metadata_parts.append(Paragraph(f"<b>Chunks encontrados:</b> {len(chunks)}", metadata_content_style))
                for i, chunk in enumerate(chunks[:3], 1):  # Limit to 3 chunks
                    if isinstance(chunk, dict):
                        chunk_id = chunk.get("chunk_id", "N/A")
                        doc_id = chunk.get("doc_id", "N/A")
                        metadata_parts.append(Paragraph(f"  • Chunk {i}: {doc_id}/{chunk_id}", metadata_content_style))
            
            # Followups
            if followups:
                metadata_parts.append(Paragraph("<b>Sugestões de próximos passos:</b>", metadata_content_style))
                for followup in followups[:3]:  # Limit to 3 followups
                    followup_escaped = _escape_html(str(followup))
                    metadata_parts.append(Paragraph(f"  • {followup_escaped}", metadata_content_style))
            
            if metadata_parts:
                return metadata_parts
    
    return None

