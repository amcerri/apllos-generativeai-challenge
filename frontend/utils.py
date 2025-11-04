"""
Utility functions for formatting and displaying content.

This module provides helper functions for formatting answers, errors, and
metadata in a user-friendly way.
"""

from __future__ import annotations

from typing import Any


def format_answer(result: dict[str, Any]) -> str:
    """Format answer text for display.

    Parameters
    ----------
    result: dict
        Result dictionary with 'text' key

    Returns
    -------
    str
        Formatted answer text
    """
    text = result.get("text", "")
    
    if not text:
        return "Nenhuma resposta disponível."
    
    # Return text as-is (preserve markdown but remove emojis)
    # Remove common emoji patterns
    import re
    # Remove emojis and special characters
    text = re.sub(r'[✅❌📊📚📄❓💡🔍⏳]', '', text)
    return text.strip()


def format_error(title: str, message: str) -> str:
    """Format error message for display.

    Parameters
    ----------
    title: str
        Error title
    message: str
        Error message

    Returns
    -------
    str
        Formatted error message
    """
    return f"{title}\n\n{message}"


def format_metadata(meta: dict[str, Any]) -> str:
    """Format metadata for display.

    Parameters
    ----------
    meta: dict
        Metadata dictionary

    Returns
    -------
    str
        Formatted metadata text
    """
    if not meta:
        return ""
    
    lines = ["**ℹ️ Informações:**\n"]
    
    # Agent information
    agent = meta.get("suggested_agent") or meta.get("agent")
    if agent:
        agent_names = {
            "analytics": "📊 Analytics",
            "knowledge": "📚 Knowledge",
            "commerce": "📄 Commerce",
            "triage": "❓ Triage",
        }
        agent_display = agent_names.get(agent, agent)
        lines.append(f"• Agente: {agent_display}")
    
    # Confidence
    confidence = meta.get("confidence")
    if confidence is not None:
        confidence_pct = float(confidence) * 100
        lines.append(f"• Confiança: {confidence_pct:.1f}%")
    
    # SQL (for analytics)
    sql = meta.get("sql")
    if sql:
        lines.append(f"• SQL: `{sql[:100]}{'...' if len(sql) > 100 else ''}`")
    
    # Document ID (for commerce)
    doc_id = meta.get("doc_id")
    if doc_id:
        lines.append(f"• Documento ID: `{doc_id}`")
    
    # Processing method (for commerce)
    method = meta.get("processing_method")
    if method:
        lines.append(f"• Método: {method}")
    
    # Row count (for analytics)
    row_count = meta.get("row_count")
    if row_count is not None:
        lines.append(f"• Linhas: {row_count}")
    
    return "\n".join(lines)

