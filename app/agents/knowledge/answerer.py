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

try:  # Optional config
    from app.config.settings import get_settings as get_config
except Exception:  # pragma: no cover - optional
    def get_config():
        return None


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

# Module-level logger for helpers outside the class
try:
    log = get_logger("agent.knowledge.answerer")
except Exception:  # pragma: no cover - optional
    import logging as _logging
    log = _logging.getLogger("agent.knowledge.answerer")


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

    def __init__(self) -> None:
        self.log = get_logger("agent.knowledge.answerer")
        self._config = get_config()
        
        # Get configuration values with fallbacks using Settings model
        try:
            answerer_cfg = getattr(getattr(self._config, "knowledge"), "answerer")  # type: ignore[attr-defined]
            self.max_citations = int(getattr(answerer_cfg, "max_citations", 5))
            self.max_chars = int(getattr(answerer_cfg, "max_chars_summary", 2000))
        except Exception:
            self.max_citations = 5
            self.max_chars = 2000

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
        max_cit = max_citations or self.max_citations
        cap_chars = max_chars or self.max_chars
        
        # CROSS-VALIDATION: Check if content is relevant to the query
        if not no_context and hits:
            relevance_score = _calculate_relevance_score(query, hits)
            
            # Enhanced relevance checking
            if relevance_score < 0.3:  # Low relevance threshold
                self.log.info("Knowledge cross-validation failed: low relevance", 
                             extra={"query": query, "relevance_score": relevance_score})
                no_context = True
            elif relevance_score < 0.5:  # Medium relevance - warn but proceed
                self.log.warning("Knowledge cross-validation: medium relevance", 
                               extra={"query": query, "relevance_score": relevance_score})
                
        # ADDITIONAL CROSS-VALIDATION: Check for conceptual questions without relevant content
        conceptual_patterns = ["como começar", "como funciona", "o que é", "estratégias", "melhores práticas"]
        is_conceptual = any(pattern in query.lower() for pattern in conceptual_patterns)
        
        if is_conceptual and not hits:
            self.log.info("Knowledge cross-validation: conceptual question without content", 
                         extra={"query": query, "is_conceptual": True})
            no_context = True

        with start_span("agent.knowledge.answer"):
            if no_context is True or not hits:
                payload = _answer_no_context_ptbr(query)
                return _coerce_answer(payload)

            citations = _make_citations(hits[:max_cit])
            # Intentionally avoid attaching raw chunks by default to keep output clean
            # Chunks remain available via helper if needed for debugging
            text = _compose_summary_ptbr(query, hits, cap_chars)

            meta = {
                "citations_count": len(citations),
                "hits_considered": min(len(hits), max_cit),
                "chunks_count": min(len(hits), max_cit),
            }
            followups = _suggest_followups(query)

            payload = {
                "text": text,
                "citations": citations,
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
    """Generate a conversational answer using LLM based on retrieved documents with response caching."""
    
    # Check response cache first
    try:
        from app.infra.cache import ResponseCache
        
        # Use singleton response cache instance
        if not hasattr(_compose_summary_ptbr, "_response_cache"):
            _compose_summary_ptbr._response_cache = ResponseCache(ttl_seconds=3600, max_size=1000)  # type: ignore[attr-defined]
        
        cache = _compose_summary_ptbr._response_cache  # type: ignore[attr-defined]
        # Create context hash from hits (doc_ids and chunk_ids)
        context = {
            "hits": [{"doc_id": h.doc_id, "chunk_id": h.chunk_id} for h in hits[:3]],
            "cap_chars": cap_chars,
        }
        cached = cache.get(query, "knowledge", context=context)
        if cached is not None and isinstance(cached, dict) and "text" in cached:
            return cached["text"]
    except Exception:
        pass
    
    # Prepare compact, relevant context from hits (salience-based, capped)
    # 1) Take up to 3 hits
    selected = list(hits[:3])
    # 2) Split into sentences and score by overlap with query tokens
    q_tokens = _tokenize(query)
    scored: list[tuple[float, str]] = []
    for i, hit in enumerate(selected, 1):
        title = hit.title or f"Documento {i}"
        for s in _split_sentences(hit.text):
            ss = s.strip()
            if not ss:
                continue
            score = _sentence_salience(q_tokens, ss)
            if score > 0:
                # Prefer sentences with higher signal; attach lightweight source tag
                scored.append((score, f"[{title}] {ss}"))
    # 3) Pick top 4 sentences and cap each to 200 chars (tighter context)
    scored.sort(key=lambda t: t[0], reverse=True)
    top_sentences = []
    for _, s in scored[:4]:
        ss = s[:200]
        top_sentences.append(ss)
    # 4) If nothing scored, fallback to trimmed heads of each hit
    if not top_sentences:
        for i, hit in enumerate(selected, 1):
            title = hit.title or f"Documento {i}"
            head = (hit.text or "").strip().splitlines()[:2]
            snippet = " ".join(x.strip() for x in head if x.strip())[:300]
            if snippet:
                top_sentences.append(f"[{title}] {snippet}")
    # 5) Build compact context (max ~1200 chars)
    context = "\n".join(top_sentences)[:1200]
    
    # Generate conversational response using LLM
    try:
        from app.infra.llm_client import get_llm_client

        client = get_llm_client()

        if not client.is_available():
            log.warning("KnowledgeAnswerer: LLM client not available; using fallback")
            raise Exception("LLM client not available")

        # Use client defaults; avoid importing settings to prevent optional deps
        model_name = getattr(client, "model", "gpt-4o-mini")
        max_tokens = 1200
        temperature = 0.5

        prompt = f"""Você é um especialista sênior em e-commerce e marketing. Responda como um humano conversando: profissional, claro, natural e coeso (pt-BR), com bom senso prático.

Pergunta: {query}

Contexto de apoio (trechos relevantes):
{context}

Instruções de formatação (texto puro, sem markdown/LaTeX):
- Sem títulos com #, sem cabeçalhos markdown
- Sem blocos de código, sem LaTeX (evite usar \[ \] ou fórmulas)
- Escreva em parágrafos, com transições suaves entre ideias (sem listas a menos que sejam essenciais)
- Se pertinente, inclua 1–2 exemplos práticos para tornar as ideias mais claras
- Encerre com recomendações acionáveis conectadas ao contexto, sem encerramentos clichê
- Evite frases soltas em linhas separadas; prefira texto contínuo com parágrafos
- Escolha o comprimento adequado ao contexto: responda o suficiente, sem padronizar tamanho

Entregue apenas o texto final, pronto para leitura em console (sem marcação)."""

        log.info(
            "KnowledgeAnswerer: calling LLM",
            extra={"model": model_name, "max_tokens": max_tokens, "temp": temperature, "context_len": len(context)},
        )
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "Você é um especialista em e-commerce que responde perguntas de forma conversacional e útil."},
                {"role": "user", "content": prompt}
            ],
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            max_retries=0
        )

        if response is None:
            log.warning("KnowledgeAnswerer: LLM response is None; using fallback")
            raise Exception("LLM response is None")

        answer = response.text.strip()
        answer = _postprocess_answer(answer, cap_chars)

        # If answer is too long, try an LLM-based compression before trimming
        if len(answer) > cap_chars:
            try:
                compress_prompt = (
                    "Resuma o texto a seguir preservando clareza, coesão e os pontos essenciais, "
                    f"em até aproximadamente {cap_chars} caracteres. Entregue apenas o texto final, sem marcação.\n\n"
                    f"Texto:\n{answer}"
                )
                comp_resp = client.chat_completion(
                    messages=[
                        {"role": "system", "content": "Você é um editor que resume mantendo fluidez e qualidade."},
                        {"role": "user", "content": compress_prompt},
                    ],
                    model=model_name,
                    max_tokens=min(max_tokens, 600),
                    temperature=0.2,
                    max_retries=0,
                )
                if comp_resp and comp_resp.text:
                    compressed = _postprocess_answer(comp_resp.text.strip(), cap_chars)
                    if compressed:
                        answer = compressed
            except Exception:
                # Ignore compression errors and fall back to smart trimming
                pass

        # Final guard: sentence-aware trimming
        if len(answer) > cap_chars:
            answer = _smart_shorten(answer, cap_chars)

        # Cache the response
        try:
            if hasattr(_compose_summary_ptbr, "_response_cache"):
                cache = _compose_summary_ptbr._response_cache  # type: ignore[attr-defined]
                context = {
                    "hits": [{"doc_id": h.doc_id, "chunk_id": h.chunk_id} for h in hits[:3]],
                    "cap_chars": cap_chars,
                }
                cache.set(query, "knowledge", {"text": answer}, context=context)
        except Exception:
            pass

        log.info("KnowledgeAnswerer: LLM answer produced", extra={"chars": len(answer)})
        return answer

    except Exception as e:
        try:
            log.warning("KnowledgeAnswerer: falling back to extractive", extra={"error": str(e)})
        except Exception:
            pass
        # Fallback to extractive summary if LLM fails — format as bullets for readability
        q_tokens = _tokenize(query)
        bullets: list[str] = []
        for idx, h in enumerate(hits[:3], 1):
            picked: list[str] = []
            for s in _split_sentences(h.text):
                score = _sentence_salience(q_tokens, s)
                if score >= 0.18:
                    picked.append(s.strip())
                if len(picked) >= 3:
                    break
            if not picked:
                head = (h.text or "").strip().splitlines()[:1]
                picked = [x.strip() for x in head if x.strip()]
            if picked:
                title = h.title or f"Documento {idx}"
                bullets.append(f"- {title}: " + " ".join(picked))

        if not bullets and hits:
            # Last resort: truncate first chunk
            snippet = (hits[0].text or "").strip()[: max(120, cap_chars // 4)]
            bullets = ["- " + snippet]

        text = "\n".join(bullets)
        if len(text) > cap_chars:
            text = text[: cap_chars - 1].rstrip() + "…"
        return _postprocess_answer(text, cap_chars)


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
            return ANSWER_CLS.from_dict(dec)  # type: ignore[attr-defined]
        if hasattr(ANSWER_CLS, "from_mapping"):
            return ANSWER_CLS.from_mapping(dec)  # type: ignore[attr-defined]
        return ANSWER_CLS(**dec)  # type: ignore[call-arg]
    except Exception:
        return dict(dec)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def _postprocess_answer(text: str, cap_chars: int) -> str:
    """Clean markdown/latex artifacts and normalize paragraphs for console output."""
    t = (text or "").strip()
    if not t:
        return t
    # Remove placeholder phrases
    forb = [
        "com base nos documentos",
        "de acordo com os documentos",
        "com base no documento",
        "de acordo com o documento",
    ]
    low = t.lower()
    for f in forb:
        if f in low:
            idx = low.find(f)
            # Drop the sentence that contains the placeholder
            # Find nearest sentence boundary after idx
            end = t.find(".", idx)
            if end != -1:
                t = (t[:idx] + t[end + 1 :]).strip()
                low = t.lower()
    # Keep postprocessing minimal to preserve LLM's conversational formatting
    import re as _re
    # Remove markdown/code/latex markers only
    t = _re.sub(r"^\s*#{1,6}\s*", "", t, flags=_re.MULTILINE)
    t = _re.sub(r"```[a-zA-Z]*\n?|```", "", t)
    t = t.replace("\\[", "").replace("\\]", "")
    # Normalize whitespace lightly
    t = _re.sub(r"[\t\x0b\f\r]+", " ", t)
    t = _re.sub(r"\n{3,}", "\n\n", t)
    # Collapse overly long bullet lists into a brief paragraph
    lines = [ln.rstrip() for ln in t.split("\n")]
    bullet_lines = [ln for ln in lines if ln.lstrip().startswith("- ")]
    if len(bullet_lines) >= 6:  # too many bullets — summarize
        # Take first 3 bullets and turn into a sentence
        top = [ln.lstrip()[2:].strip() for ln in bullet_lines[:3] if len(ln.lstrip()) > 2]
        if top:
            summary = "; ".join(top)
            t = _re.sub(r"(^|\n)- .*", "", t)
            t = (t.strip() + "\n\nPrincipais pontos: " + summary + ".").strip()
        # Normalize whitespace again after transformation
        t = _re.sub(r"[ \t\x0b\f\r]+", " ", t)
        t = _re.sub(r"\n{3,}", "\n\n", t)
    # Cap length
    if len(t) > cap_chars:
        t = t[: cap_chars - 1].rstrip() + "..."
    return t


def _suggest_followups(query: str) -> list[str]:
    # Provide objective follow‑up questions in pt‑BR
    base = [
        "Pode fornecer mais detalhes?",
        "Tem algum documento específico para anexar?",
        "Gostaria de perguntar algo mais específico?",
    ]
    return base


def _smart_shorten(text: str, cap_chars: int) -> str:
    """Trim at the nearest sentence boundary under cap; fallback to hard cut with ellipsis."""
    t = (text or "").strip()
    if len(t) <= cap_chars:
        return t
    # Try to cut at last full stop within cap
    candidate = t[:cap_chars]
    last_dot = candidate.rfind(".")
    last_exc = candidate.rfind("!")
    last_q = candidate.rfind("?")
    cut = max(last_dot, last_exc, last_q)
    if cut >= max(60, int(cap_chars * 0.6)):
        return candidate[:cut + 1].strip()
    # Fallback: cut at last space and add ellipsis
    last_space = candidate.rfind(" ")
    if last_space > 0:
        return (candidate[:last_space].rstrip() + "...")
    return candidate.rstrip() + "..."


def _calculate_relevance_score(query: str, hits: Sequence[HitLike]) -> float:
    """Calculate relevance score between query and hits."""
    if not hits:
        return 0.0
        
    query_lower = query.lower()
    query_terms = set(re.findall(r'\b\w+\b', query_lower))
    
    total_score = 0.0
    hit_count = 0
    
    for hit in hits[:5]:  # Check top 5 hits
        hit_text = hit.text.lower()
        hit_terms = set(re.findall(r'\b\w+\b', hit_text))
        
        # Calculate term overlap
        overlap = len(query_terms.intersection(hit_terms))
        if query_terms:
            term_score = overlap / len(query_terms)
        else:
            term_score = 0.0
            
        # Calculate semantic similarity (simple keyword matching)
        semantic_score = 0.0
        for term in query_terms:
            if term in hit_text:
                semantic_score += 1.0
                
        if query_terms:
            semantic_score = semantic_score / len(query_terms)
            
        # Combined score
        hit_score = (term_score + semantic_score) / 2.0
        total_score += hit_score
        hit_count += 1
        
    return total_score / hit_count if hit_count > 0 else 0.0
