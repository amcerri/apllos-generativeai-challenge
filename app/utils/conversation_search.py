"""
Conversation history semantic search with topic shift detection.

Overview
  Provides semantic search capabilities for conversation history, allowing
  retrieval of relevant previous messages based on semantic similarity. Includes
  topic shift detection to prevent using irrelevant context and relevance
  validation to ensure context is appropriate for the current query.

Design
  - Uses embeddings for semantic similarity calculation
  - Detects topic shifts to avoid using irrelevant context
  - Validates context relevance before returning
  - Supports finding referenced messages and relevant context
  - Graceful degradation when LLM client is unavailable

Integration
  - Used by routing system to inject relevant context
  - Integrates with LLM client for embeddings
  - Uses embedding cache when available

Usage
  >>> from app.utils.conversation_search import ConversationHistorySearcher
  >>> searcher = ConversationHistorySearcher()
  >>> context = searcher.get_relevant_context(
  ...     current_query="E sobre o estado de SP?",
  ...     conversation_history=[{"role": "user", "content": "Mostre vendas por estado"}]
  ... )
  >>> context["is_relevant"]
  True
"""

from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Mapping, Sequence
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

try:
    from app.infra.cache import EmbeddingCache
except Exception:
    EmbeddingCache = None

__all__ = ["ConversationHistorySearcher"]


class ConversationHistorySearcher:
    """Semantic search in conversation history for relevant context retrieval."""

    def __init__(self) -> None:
        """Initialize conversation history searcher."""
        self.log = get_logger(__name__)
        self._llm_client = None
        self._embedding_cache = None

        try:
            if get_llm_client:
                self._llm_client = get_llm_client()
        except Exception:
            pass

        try:
            if EmbeddingCache:
                self._embedding_cache = EmbeddingCache(ttl_seconds=86400, max_size=5000)
        except Exception:
            pass

    def find_relevant_messages(
        self,
        current_query: str,
        conversation_history: list[dict[str, Any]],
        max_messages: int = 5,
    ) -> list[dict[str, Any]]:
        """Find relevant previous messages for the current query.

        Uses embeddings to search for semantically similar messages, not just
        the last message. Allows resuming previous conversations.

        Parameters
        ----------
        current_query
            Current user query.
        conversation_history
            List of previous messages (user/assistant).
        max_messages
            Maximum number of relevant messages to return.

        Returns
        -------
        list[dict[str, Any]]
            List of relevant messages ordered by relevance.
        """
        if not conversation_history:
            return []

        query_embedding = self._get_embedding(current_query)

        scored_messages = []
        for msg in conversation_history:
            content = msg.get("content", "") or msg.get("text", "")
            if not content:
                continue

            msg_embedding = self._get_embedding(content)
            similarity = self._cosine_similarity(query_embedding, msg_embedding)

            scored_messages.append(
                {
                    "message": msg,
                    "similarity": similarity,
                    "content": content,
                }
            )

        scored_messages.sort(key=lambda x: x["similarity"], reverse=True)
        relevant = scored_messages[:max_messages]

        # Lower threshold for follow-up detection - queries like "E por estado?" should match
        # previous queries even with lower similarity
        min_similarity = 0.25
        # Always include the last message if it's from assistant (most recent context)
        if conversation_history:
            last_msg = conversation_history[-1]
            if last_msg.get("role") == "assistant":
                # Include last assistant message even if similarity is lower (it's the most recent context)
                for scored in scored_messages:
                    if scored["message"] == last_msg and scored["similarity"] >= 0.15:
                        if scored not in relevant:
                            relevant.append(scored)
                            relevant.sort(key=lambda x: x["similarity"], reverse=True)
                            relevant = relevant[:max_messages]
                        break

        relevant = [m for m in relevant if m["similarity"] >= min_similarity]

        return [m["message"] for m in relevant]

    def detect_referenced_message(
        self,
        current_query: str,
        conversation_history: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Detect which previous message is being referenced.

        Uses LLM to identify explicit or implicit references to previous
        messages in the conversation.

        Parameters
        ----------
        current_query
            Current query that may reference a previous message.
        conversation_history
            Complete conversation history.

        Returns
        -------
        dict[str, Any] | None
            Referenced message or None if none detected.
        """
        if not conversation_history:
            return None

        reference_patterns = [
            r"\b(sobre|acerca de|relacionado a|sobre o que|sobre a)\s+(isso|aquilo|aquela|aquele)",
            r"\b(na|da|do|no|naquela|naquele)\s+(resposta|mensagem|pergunta anterior)",
            r"\b(que você disse|que eu perguntei|que falamos)",
            r"\b(voltar|retomar|continuar)\s+(sobre|com|a)",
        ]

        has_explicit_reference = any(
            re.search(p, current_query, re.IGNORECASE) for p in reference_patterns
        )

        if not has_explicit_reference:
            relevant = self.find_relevant_messages(current_query, conversation_history, max_messages=1)
            if relevant:
                query_emb = self._get_embedding(current_query)
                msg_emb = self._get_embedding(relevant[0].get("content", ""))
                similarity = self._cosine_similarity(query_emb, msg_emb)
                if similarity > 0.5:
                    return relevant[0]
            return None

        if not self._llm_client or not self._llm_client.is_available():
            return None

        context = "\n".join(
            [
                f"{i+1}. {msg.get('role', 'user')}: {msg.get('content', '')}"
                for i, msg in enumerate(conversation_history[-10:])
            ]
        )

        detection_prompt = f"""
        O usuário fez uma pergunta que referencia uma mensagem anterior na conversa.

        PERGUNTA ATUAL: {current_query}

        HISTÓRICO DA CONVERSA:
        {context}

        Identifique qual mensagem anterior (por número) está sendo referenciada.
        Se nenhuma mensagem específica for referenciada, retorne null.

        Retorne JSON: {{"referenced_message_index": int | null, "reason": "string"}}
        """

        try:
            response = self._llm_client.chat_completion(
                messages=[{"role": "user", "content": detection_prompt}],
                model="gpt-4o-mini",
                temperature=0.0,
                max_tokens=200,
            )
            if not response or not response.text:
                return None

            result = self._llm_client.extract_json(response.text)
            idx = result.get("referenced_message_index")

            if idx is not None and 0 <= idx < len(conversation_history):
                return conversation_history[idx]
        except Exception as exc:
            self.log.debug("Failed to detect referenced message", extra={"error": str(exc)})

        return None

    def detect_topic_shift(
        self,
        current_query: str,
        conversation_history: list[dict[str, Any]],
        threshold: float = 0.3,
    ) -> bool:
        """Detect if the current query represents a topic shift.

        Compares the current query with recent history to determine if it is
        a continuation of the topic or a new question.

        Parameters
        ----------
        current_query
            Current user query.
        conversation_history
            Complete conversation history.
        threshold
            Similarity threshold below which a topic shift is considered.

        Returns
        -------
        bool
            True if topic shift detected, False otherwise.
        """
        if not conversation_history:
            return False

        new_question_patterns = [
            r"^(agora|e agora|outra|outro|diferente|mudando|mudar de assunto)",
            r"^(e se|e sobre|e quanto|e qual)",
            r"^(vamos|vou|quero|preciso|gostaria)\s+(falar|perguntar|saber)\s+(sobre|de)",
        ]

        has_explicit_new_question = any(
            re.search(p, current_query, re.IGNORECASE) for p in new_question_patterns
        )

        if has_explicit_new_question:
            return True

        recent_history = conversation_history[-5:]
        if not recent_history:
            return False

        query_embedding = self._get_embedding(current_query)

        similarities = []
        for msg in recent_history:
            content = msg.get("content", "") or msg.get("text", "")
            if not content:
                continue

            msg_embedding = self._get_embedding(content)
            similarity = self._cosine_similarity(query_embedding, msg_embedding)
            similarities.append(similarity)

        if not similarities:
            return False

        avg_similarity = sum(similarities) / len(similarities)
        max_similarity = max(similarities)

        topic_shift = avg_similarity < threshold and max_similarity < (threshold + 0.1)

        return topic_shift

    def validate_context_relevance(
        self,
        current_query: str,
        context_messages: list[dict[str, Any]],
        min_relevance: float = 0.25,
    ) -> bool:
        """Validate if historical context is relevant for the current query.

        Verifies that context messages have sufficient similarity with the
        current query to justify their use.

        Parameters
        ----------
        current_query
            Current user query.
        context_messages
            Context messages to validate.
        min_relevance
            Minimum similarity to consider relevant.

        Returns
        -------
        bool
            True if context is relevant, False otherwise.
        """
        if not context_messages:
            return False

        query_embedding = self._get_embedding(current_query)

        relevances = []
        for msg in context_messages:
            content = msg.get("content", "")
            if not content:
                continue

            msg_embedding = self._get_embedding(content)
            similarity = self._cosine_similarity(query_embedding, msg_embedding)
            relevances.append(similarity)

        if not relevances:
            return False

        max_relevance = max(relevances)
        avg_relevance = sum(relevances) / len(relevances)

        is_relevant = max_relevance >= min_relevance and avg_relevance >= (min_relevance - 0.1)

        return is_relevant

    def get_relevant_context(
        self,
        current_query: str,
        conversation_history: list[dict[str, Any]],
        last_answer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Get relevant context for the current query with relevance validation.

        Combines last answer with semantically relevant messages from history,
        but only if validated as relevant. Protects against using irrelevant
        context for new questions.

        Parameters
        ----------
        current_query
            Current user query.
        conversation_history
            Complete conversation history.
        last_answer
            Last assistant answer if available.

        Returns
        -------
        dict[str, Any]
            Dictionary with relevant context or empty if not relevant.
        """
        # Use LLM to detect if this is a follow-up (language-agnostic)
        # Fallback to keyword patterns only if LLM unavailable
        is_followup = self._detect_followup_llm(current_query, conversation_history, last_answer)
        
        # Only check topic shift if we have history
        # If LLM detected it's a follow-up, don't treat as topic shift
        topic_shift = False
        if conversation_history:
            topic_shift = self.detect_topic_shift(current_query, conversation_history)
            # If LLM confirmed it's a follow-up, override topic shift detection
            if is_followup:
                topic_shift = False
        elif is_followup and last_answer:
            # If it's a follow-up and we have last_answer, assume it's relevant
            topic_shift = False

        if topic_shift:
            return {
                "relevant_messages": [],
                "context_summary": "",
                "is_relevant": False,
                "reason": "topic_shift_detected",
            }

        context_messages = []

        # Always include last_answer if available (it's the most recent context)
        if last_answer:
            last_content = last_answer.get("text", "")
            if last_content:
                context_messages.append(
                    {
                        "type": "last_answer",
                        "content": last_content,
                        "agent": last_answer.get("meta", {}).get("agent"),
                        "timestamp": "most_recent",
                    }
                )

        relevant_messages = self.find_relevant_messages(
            current_query,
            conversation_history,
            max_messages=3,
        )

        for msg in relevant_messages:
            context_messages.append(
                {
                    "type": "relevant_history",
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "") or msg.get("text", ""),
                    "timestamp": msg.get("timestamp"),
                }
            )

        referenced = self.detect_referenced_message(current_query, conversation_history)
        if referenced:
            ref_content = referenced.get("content", "") or referenced.get("text", "")
            if ref_content:
                already_included = any(
                    msg.get("content", "") == ref_content for msg in context_messages
                )
                if not already_included:
                    context_messages.insert(
                        0,
                        {
                            "type": "referenced",
                            "role": referenced.get("role", "user"),
                            "content": ref_content,
                            "timestamp": referenced.get("timestamp"),
                        },
                    )

        # If we have last_answer but no other context, still use it for follow-ups
        if not context_messages and last_answer and is_followup:
            last_content = last_answer.get("text", "")
            if last_content:
                context_messages.append(
                    {
                        "type": "last_answer",
                        "content": last_content,
                        "agent": last_answer.get("meta", {}).get("agent"),
                        "timestamp": "most_recent",
                    }
                )
        
        if not context_messages:
            return {
                "relevant_messages": [],
                "context_summary": "",
                "is_relevant": False,
                "reason": "no_context_available",
            }

        # For follow-ups detected by LLM, be more permissive with relevance
        # If we have last_answer and it's a follow-up, assume it's relevant
        is_relevant = False
        if is_followup and last_answer:
            # LLM-confirmed follow-ups with last_answer are assumed relevant
            is_relevant = True
        else:
            is_relevant = self.validate_context_relevance(current_query, context_messages)

        if not is_relevant:
            return {
                "relevant_messages": [],
                "context_summary": "",
                "is_relevant": False,
                "reason": "low_relevance_threshold",
            }

        return {
            "relevant_messages": context_messages,
            "context_summary": self._summarize_context(context_messages),
            "is_relevant": True,
            "reason": "validated_relevant",
        }

    def _detect_followup_llm(
        self,
        current_query: str,
        conversation_history: list[dict[str, Any]],
        last_answer: dict[str, Any] | None = None,
    ) -> bool:
        """Detect if current query is a follow-up using LLM (language-agnostic).
        
        Uses LLM as primary method, falls back to keyword patterns only if LLM unavailable.
        
        Parameters
        ----------
        current_query
            Current user query.
        conversation_history
            Previous conversation messages.
        last_answer
            Last assistant answer if available.
            
        Returns
        -------
        bool
            True if query is detected as follow-up, False otherwise.
        """
        if not current_query or not current_query.strip():
            return False
        
        # If no context at all, can't be a follow-up
        if not conversation_history and not last_answer:
            return False
        
        # Try LLM first (language-agnostic)
        if self._llm_client and self._llm_client.is_available():
            try:
                context_parts = []
                if conversation_history:
                    for msg in conversation_history[-3:]:
                        role = msg.get("role", "user")
                        content = msg.get("content", "") or msg.get("text", "")
                        if content:
                            context_parts.append(f"{role.upper()}: {content}")
                
                if last_answer and not conversation_history:
                    last_content = last_answer.get("text", "") if isinstance(last_answer, dict) else str(last_answer)
                    if last_content:
                        context_parts.append(f"ASSISTANT: {last_content}")
                
                if not context_parts:
                    return False
                
                context = "\n".join(context_parts)
                
                detection_prompt = f"""Determine if the current user query is a follow-up question to the previous conversation.

CURRENT QUERY: {current_query}

CONVERSATION CONTEXT:
{context}

A follow-up question:
- References or continues the previous topic
- Uses pronouns, demonstratives, or implicit references
- Starts with connecting words (and, but, also, what about, etc.)
- Is incomplete without the previous context

Respond with ONLY "yes" or "no" (lowercase, no punctuation, no explanation).
"""
                
                response = self._llm_client.chat_completion(
                    messages=[{"role": "user", "content": detection_prompt}],
                    model="gpt-4o-mini",
                    temperature=0.0,
                    max_tokens=10,
                )
                
                if response and response.text:
                    result = response.text.strip().lower()
                    is_followup = result.startswith("yes")
                    if is_followup:
                        self.log.debug("Follow-up detected via LLM", extra={"query": current_query[:50]})
                    return is_followup
            except Exception as exc:
                self.log.debug("LLM follow-up detection failed, using fallback", extra={"error": str(exc)})
        
        # Fallback: keyword patterns (language-specific, only when LLM unavailable)
        followup_patterns = [
            r"^(and|e|mas|but|também|also|what about|e sobre)\s+",
            r"^(and|e|mas|but|também|also)\s+(by|por|about|sobre|for|para|of|de|how|quanto|qual)",
            r"^(what about|e sobre|e quanto|and how many|and what)",
        ]
        
        has_followup_pattern = any(
            re.search(p, current_query, re.IGNORECASE) for p in followup_patterns
        )
        
        return has_followup_pattern

    def _get_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using LLM client or fallback."""
        if not text or not text.strip():
            return self._hash_embedding(text)

        cached = None
        if self._embedding_cache:
            try:
                cached = self._embedding_cache.get(text, "text-embedding-3-small")
            except Exception:
                pass

        if cached is not None:
            return cached

        vec: list[float] | None = None
        if self._llm_client and self._llm_client.is_available():
            try:
                vec_result = self._llm_client.get_embeddings(text=text, model="text-embedding-3-small")
                if vec_result and isinstance(vec_result, list):
                    vec = vec_result[0] if (len(vec_result) > 0 and isinstance(vec_result[0], list)) else vec_result  # type: ignore[assignment]
            except Exception:
                pass

        if vec is not None:
            if self._embedding_cache:
                try:
                    self._embedding_cache.set(text, "text-embedding-3-small", vec)
                except Exception:
                    pass
            return vec

        return self._hash_embedding(text)

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def _hash_embedding(self, text: str) -> list[float]:
        """Fallback: hash-based embedding for when LLM is unavailable."""
        dim = 1536
        vec = [0.0] * dim
        for word in text.lower().split():
            h = hashlib.md5(word.encode()).hexdigest()
            idx = int(h[:8], 16) % dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def _summarize_context(self, context_messages: list[dict[str, Any]]) -> str:
        """Generate context summary for prompt injection."""
        if not context_messages:
            return ""

        summary_parts = []
        for msg in context_messages:
            msg_type = msg.get("type", "unknown")
            content = msg.get("content", "")[:200]

            if msg_type == "last_answer":
                summary_parts.append(f"[Última resposta] {content}")
            elif msg_type == "referenced":
                summary_parts.append(f"[Mensagem referenciada] {content}")
            elif msg_type == "relevant_history":
                role = msg.get("role", "user")
                summary_parts.append(f"[Histórico - {role}] {content}")

        return "\n".join(summary_parts)

