"""
Knowledge answerer (PT‑BR composition with citations).

Overview
--------
Compose a user‑facing answer in Portuguese (pt‑BR) from ranked RAG hits,
including mandatory citations. When there is insufficient context, return an
Answer‑like payload with `no_context=True` and objective follow‑ups.

Design
------
- Inputs: user `query` and ranked hits from the retriever/ranker.
- Output: `Answer` dataclass (if available) or a plain `dict` with keys:
  `text`, `citations`, `meta`, and optional `followups`.
- Summarization is conservative/extractive: pick salient sentences from
  the top chunks; no additional LLM calls in this POC.
- Citations: one entry per cited chunk (title, url|doc_id, chunk_id, lines).

Integration
-----------
Called by the knowledge agent after retrieval and ranking, before returning to
the graph. Keep answers concise and business‑oriented.

Usage
-----
>>> from app.agents.knowledge.answerer import KnowledgeAnswerer
>>> ans = KnowledgeAnswerer().answer("Qual a política de frete?", ranked=[])
>>> isinstance(ans, dict) or hasattr(ans, "text")
True
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final, Protocol, runtime_checkable

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


# Tracing (optional; single alias)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# Optional Answer dataclass
ANSWER_CLS: Any
try:
    from app.contracts.answer import Answer as _Answer

    ANSWER_CLS = _Answer
except Exception:  # pragma: no cover - optional
    ANSWER_CLS = None

__all__ = ["KnowledgeAnswerer"]


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------
@runtime_checkable
class HitLike(Protocol):
    doc_id: str
    chunk_id: str
    title: str | None
    text: str
    source: str | None


@dataclass(slots=True)
class _HitView:
    doc_id: str
    chunk_id: str
    title: str | None
    text: str
    source: str | None


# ---------------------------------------------------------------------------
# Answerer
# ---------------------------------------------------------------------------
class KnowledgeAnswerer:
    """Compose pt‑BR answers from RAG hits with mandatory citations."""

    MAX_CITATIONS: Final[int] = 5
    MAX_CHARS: Final[int] = 2000

    def __init__(self) -> None:
        self.log = get_logger("agent.knowledge.answerer")

    def answer(
        self,
        query: str,
        ranked: Sequence[HitLike] | Sequence[Mapping[str, Any]],
        *,
        max_citations: int | None = None,
        max_chars: int | None = None,
        no_context: bool | None = None,
    ) -> Any:
        """Return an Answer-like object with `text` in pt-BR and citations.

        Parameters
        ----------
        query: User question in natural language.
        ranked: Ranked retrieval hits.
        max_citations: Cap on number of citations included (default: 5).
        max_chars: Soft cap for answer text size (default: 900 chars).
        no_context: Force `no_context=True` regardless of hits.
        """

        hits = _coerce_hits(ranked)
        max_cit = max_citations or self.MAX_CITATIONS
        cap_chars = max_chars or self.MAX_CHARS

        with start_span("agent.knowledge.answer"):
            if no_context is True or not hits:
                payload = _answer_no_context_ptbr(query)
                return _coerce_answer(payload)

            citations = _make_citations(hits[:max_cit])
            chunks = _make_chunks(hits[:max_cit])  # Add chunks to payload
            text = _compose_summary_ptbr(query, hits, cap_chars)

            meta = {
                "citations_count": len(citations),
                "hits_considered": min(len(hits), max_cit),
                "chunks_count": len(chunks),
            }
            followups = _suggest_followups(query)

            payload = {
                "text": text,
                "citations": citations,
                "chunks": chunks,  # Include chunks in payload
                "meta": meta,
                "followups": followups,
            }
            return _coerce_answer(payload)


# ---------------------------------------------------------------------------
# Coercion & utils
# ---------------------------------------------------------------------------


def _coerce_hits(seq: Sequence[HitLike] | Sequence[Mapping[str, Any]]) -> list[_HitView]:
    out: list[_HitView] = []
    for h in seq:
        if isinstance(h, Mapping):
            out.append(
                _HitView(
                    doc_id=str(h.get("doc_id", "")),
                    chunk_id=str(h.get("chunk_id", "")),
                    title=str(h.get("title")) if h.get("title") is not None else None,
                    text=str(h.get("text", "")),
                    source=str(h.get("source")) if h.get("source") is not None else None,
                )
            )
        else:
            # Protocol conformance assumed at runtime
            out.append(
                _HitView(
                    doc_id=h.doc_id,
                    chunk_id=h.chunk_id,
                    title=h.title,
                    text=h.text,
                    source=h.source,
                )
            )
    return out


def _answer_no_context_ptbr(query: str) -> dict[str, Any]:
    t = (query or "").strip()
    text = (
        "Não encontrei base suficiente nos documentos para responder com segurança. "
        "Você pode: (1) anexar o material relevante (PDF/TXT), (2) reformular com mais detalhes, "
        "ou (3) perguntar algo mais específico."
    )
    return {
        "text": text,
        "no_context": True,
        "followups": _suggest_followups(t),
        "citations": [],
        "meta": {"citations_count": 0, "hits_considered": 0},
    }


def _compose_summary_ptbr(query: str, hits: Sequence[_HitView], cap_chars: int) -> str:
    """Generate a conversational answer using LLM based on retrieved documents."""
    
    # Prepare context from hits
    context_parts = []
    for i, hit in enumerate(hits[:5], 1):  # Use top 5 hits
        title = hit.title or f"Documento {i}"
        content = hit.text.strip()
        context_parts.append(f"[{title}]\n{content}\n")
    
    context = "\n".join(context_parts)
    
    # Generate conversational response using LLM
    try:
        from openai import OpenAI
        import os
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""Você é um assistente especializado em e-commerce. Com base nos documentos fornecidos, responda à pergunta de forma conversacional e natural, como se estivesse conversando com alguém.

Pergunta: {query}

Documentos relevantes:
{context}

Instruções:
- Responda de forma direta e conversacional
- Use as informações dos documentos para fundamentar sua resposta
- Não mencione "de acordo com os documentos" ou similar
- Seja útil e prático
- Use linguagem natural e acessível
- Foque em responder especificamente à pergunta feita

Resposta:"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em e-commerce que responde perguntas de forma conversacional e útil."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Cap length if needed
        if len(answer) > cap_chars:
            answer = answer[:cap_chars - 1].rstrip() + "..."
            
        return answer
        
    except Exception as e:
        # Fallback to extractive summary if LLM fails
        q_tokens = _tokenize(query)
        sentences: list[str] = []
        for h in hits[:3]:
            for s in _split_sentences(h.text):
                score = _sentence_salience(q_tokens, s)
                if score >= 0.15:
                    sentences.append(s.strip())
            if len(sentences) >= 8:
                break

        if not sentences:
            fallback = hits[0].text.strip().splitlines()[0:2]
            text = " ".join(x.strip() for x in fallback if x.strip())
        else:
            seen: set[str] = set()
            uniq: list[str] = []
            for s in sentences:
                if s not in seen:
                    clean_s = s.strip()
                    if clean_s and not clean_s.endswith('.'):
                        clean_s += '.'
                    uniq.append(clean_s)
                    seen.add(s)
            text = " ".join(uniq)

        if len(text) > cap_chars:
            text = text[:cap_chars - 1].rstrip() + "…"
            
        return f"Com base nos documentos disponíveis: {text}"


def _make_citations(hits: Sequence[_HitView]) -> list[dict[str, Any]]:
    cites: list[dict[str, Any]] = []
    for h in hits:
        item: dict[str, Any] = {
            "title": h.title or "(sem título)",
            "chunk_id": h.chunk_id,
            "lines": "",
        }
        if _looks_like_url(h.source or ""):
            item["url"] = h.source
        else:
            item["doc_id"] = h.doc_id
        cites.append(item)
    return cites


def _make_chunks(hits: Sequence[_HitView]) -> list[dict[str, Any]]:
    """Create chunks payload with full text content for each hit."""
    chunks: list[dict[str, Any]] = []
    for i, h in enumerate(hits, 1):
        chunk = {
            "id": f"chunk_{i}",
            "title": h.title or f"Documento {i}",
            "doc_id": h.doc_id,
            "chunk_id": h.chunk_id,
            "content": h.text.strip(),
            "source": h.source,
        }
        chunks.append(chunk)
    return chunks


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_\-]+", flags=re.IGNORECASE)


def _split_sentences(text: str) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    # Normalize newlines to spaces, then split on sentence boundaries
    normalized = re.sub(r"\s*\n+\s*", " ", text)
    parts = _SENT_SPLIT_RE.split(normalized)
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> set[str]:
    return {m.group(0).lower() for m in _TOKEN_RE.finditer(text or "")}


def _sentence_salience(q_tokens: set[str], sent: str) -> float:
    if not q_tokens or not sent:
        return 0.0
    s_tokens = _tokenize(sent)
    if not s_tokens:
        return 0.0
    inter = len(q_tokens & s_tokens)
    return inter / max(1, len(q_tokens))


def _looks_like_url(s: str) -> bool:
    return bool(re.match(r"^https?://", s))


# ---------------------------------------------------------------------------
# Answer coercion
# ---------------------------------------------------------------------------


def _coerce_answer(dec: Mapping[str, Any]) -> Any:
    if ANSWER_CLS is None:
        return dict(dec)
    try:
        if hasattr(ANSWER_CLS, "from_dict"):
            return ANSWER_CLS.from_dict(dec)
        if hasattr(ANSWER_CLS, "from_mapping"):
            return ANSWER_CLS.from_mapping(dec)
        return ANSWER_CLS(**dec)
    except Exception:
        return dict(dec)


def _suggest_followups(query: str) -> list[str]:
    # Provide objective follow‑up questions in pt‑BR
    base = [
        "Pode fornecer mais detalhes?",
        "Tem algum documento específico para anexar?",
        "Gostaria de perguntar algo mais específico?",
    ]
    return base
