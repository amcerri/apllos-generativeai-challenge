"""
Anaphora resolution and follow-up detection for conversational context.

Overview
  Resolves anaphoric references (pronouns, demonstratives) and detects follow-up
  questions in user queries using conversation history. Uses LLM as primary method
  for language-agnostic detection, with keyword patterns as fallback only.

Design
  - LLM-first approach for anaphora and follow-up detection (language-agnostic)
  - Pattern-based fallback when LLM is unavailable
  - Graceful degradation when LLM is unavailable
  - Integration with conversation history

Integration
  - Used by routing system before classification
  - Integrates with conversation history searcher
  - Works with LLM client for resolution

Usage
  >>> from app.utils.anaphora import resolve_anaphora
  >>> resolved = resolve_anaphora(
  ...     query="E sobre isso?",
  ...     conversation_history=[{"role": "user", "content": "Mostre vendas por estado"}]
  ... )
  >>> "vendas por estado" in resolved.lower()
  True
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

try:
    from app.infra.logging import get_logger
except Exception:
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:
    from app.infra.llm_client import get_llm_client
except Exception:
    get_llm_client = None

__all__ = ["resolve_anaphora"]


def resolve_anaphora(
    query: str,
    conversation_history: Sequence[dict[str, Any]] | None = None,
    last_answer: dict[str, Any] | None = None,
) -> str:
    """Resolve anaphoric references and follow-ups in query using conversation history.

    Uses LLM as primary method to detect follow-ups and resolve anaphoric references
    in a language-agnostic way. Falls back to keyword patterns only when LLM is unavailable.

    Parameters
    ----------
    query
        User query that may contain anaphoric references or be a follow-up.
    conversation_history
        Previous conversation messages for context.
    last_answer
        Last assistant answer if available (used when history is empty).

    Returns
    -------
    str
        Query with resolved references and expanded context, or original query if no resolution needed.
    """
    if not query or not query.strip():
        return query

    # If no history and no last_answer, nothing to resolve
    if not conversation_history and not last_answer:
        return query

    llm_client = None
    try:
        if get_llm_client:
            llm_client = get_llm_client()
    except Exception:
        pass

    # Build context from history and last_answer
    context_parts = []
    if conversation_history:
        for msg in conversation_history[-5:]:  # Last 5 messages
            role = msg.get("role", "user")
            content = msg.get("content", "") or msg.get("text", "")
            if content:
                context_parts.append(f"{role.upper()}: {content}")
    
    if last_answer and not conversation_history:
        # If no history but we have last_answer, use it as context
        last_content = last_answer.get("text", "") if isinstance(last_answer, dict) else str(last_answer)
        if last_content:
            context_parts.append(f"ASSISTANT: {last_content}")

    if not context_parts:
        return query

    context = "\n".join(context_parts)

    # LLM-first approach: always try LLM if available
    if llm_client and llm_client.is_available():
        try:
            log = get_logger(__name__)
            
            # Language-agnostic prompt that works for any language
            resolution_prompt = f"""Analyze if the current user query is a follow-up question or contains anaphoric references (pronouns, demonstratives) that need to be resolved using the conversation context.

CURRENT QUERY: {query}

CONVERSATION CONTEXT:
{context}

If the current query is a follow-up to the previous conversation, expand it to include the necessary context.
For example, if the context mentions "orders" and the current query is "And by state?", expand to "orders by state".

If there are anaphoric references (pronouns, demonstratives like "this", "that", "it", "the same"), replace them with explicit content from the context.

Keep the resolved query natural and clear. Maintain the original language of the query.

Return ONLY the resolved and expanded query, without any explanations or additional text.
"""

            response = llm_client.chat_completion(
                messages=[{"role": "user", "content": resolution_prompt}],
                model="gpt-4o-mini",
                temperature=0.0,
                max_tokens=200,
            )
            if response and response.text:
                resolved = response.text.strip()
                # Remove quotes if LLM added them
                resolved = resolved.strip('"\'')
                if resolved and resolved != query and len(resolved) > len(query) * 0.5:
                    log.debug("Anaphora/follow-up resolved via LLM", 
                            extra={"original": query[:50], "resolved": resolved[:50]})
                    return resolved
        except Exception as exc:
            log = get_logger(__name__)
            log.debug("LLM anaphora resolution failed, using fallback", extra={"error": str(exc)})

    # Fallback: keyword-based detection (only when LLM unavailable)
    # This is language-specific but better than nothing
    anaphora_patterns = [
        r"\b(this|that|it|these|those|ele|ela|eles|elas|isso|aquilo)\b",
        r"\b(the same|o mesmo|a mesma|os mesmos|as mesmas)\b",
        r"\b(that|those|esse|essa|esses|essas|aquele|aquela)\b",
    ]

    # Follow-up patterns (language-specific fallback)
    followup_patterns = [
        r"^(and|e|mas|but|também|also)\s+(by|por|about|sobre|for|para|of|de)",
        r"^(and|e|mas|but|também|also)\s+",
        r"^(what about|e sobre|e quanto|and how many)",
    ]

    has_anaphora = any(re.search(p, query, re.IGNORECASE) for p in anaphora_patterns)
    has_followup_pattern = any(re.search(p, query, re.IGNORECASE) for p in followup_patterns)

    # If no patterns detected in fallback, return original
    if not has_anaphora and not has_followup_pattern:
        return query

    # Fallback: simple expansion using last message context
    # This is a very basic fallback - LLM is much better
    # If we reach here, LLM was unavailable and patterns didn't match
    # Return original query as we can't safely expand it
    return query

