"""
Knowledge ranker (lightweight heuristic reordering).

Overview
--------
Re-rank retrieval hits using simple, deterministic signals on top of the
embedding similarity score:
- Query term overlap in **title** and **chunk text**;
- Exact-phrase boost when the full query appears verbatim;
- Gentle penalties for overly short/long chunks to prefer informative snippets.

Design
------
- Inputs: `query: str` and a sequence of retrieval hits (from the retriever).
- Output: ranked hits with an additional `rerank` score (0..1).
- Deterministic, pure-Python; no network calls or external deps.
- Stable ordering: ties are broken by original similarity, then by length.

Integration
-----------
- Use right after the retriever and before the answerer in the knowledge agent.
- Compatible with the `RetrievalHit` dataclass from
  `app.agents.knowledge.retriever`; if it's unavailable at import time, a local
  minimal fallback dataclass is provided to keep tests runnable.

Usage
-----
>>> from app.agents.knowledge.ranker import KnowledgeRanker
>>> rk = KnowledgeRanker()
>>> ranked = rk.rank("política de devolução Olist", hits=[], top_k=5)
>>> isinstance(ranked.hits, list)
True
"""

from __future__ import annotations

import math
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


# Tracing (optional; keep a single alias to avoid mypy signature clashes)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span


@runtime_checkable
class RetrievalHitLike(Protocol):
    doc_id: str
    chunk_id: str
    score: float
    title: str | None
    text: str
    source: str | None
    metadata: dict[str, Any]


__all__ = ["RankedHit", "RankResult", "KnowledgeRanker"]


# ---------------------------------------------------------------------------
# Result contracts
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class RankedHit:
    """Hit with the original similarity and the computed rerank score."""

    doc_id: str
    chunk_id: str
    score: float  # original similarity from retriever
    rerank: float  # final score after heuristic signals (0..1)
    title: str | None
    text: str
    source: str | None
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id,
            "score": float(self.score),
            "rerank": float(self.rerank),
            "title": self.title,
            "text": self.text,
            "source": self.source,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class RankResult:
    """Ranker output with diagnostics."""

    hits: list[RankedHit]
    used_weights: Mapping[str, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "hits": [h.to_dict() for h in self.hits],
            "used_weights": dict(self.used_weights),
        }


# ---------------------------------------------------------------------------
# Ranker
# ---------------------------------------------------------------------------
class KnowledgeRanker:
    """Lightweight heuristic re-ranker for document chunks."""

    # Weights (tuned conservatively; base similarity dominates)
    W_BASE: Final[float] = 1.00
    W_TITLE: Final[float] = 0.15
    W_BODY: Final[float] = 0.10
    W_PHRASE: Final[float] = 0.20

    # Soft penalties
    PEN_SHORT: Final[float] = 0.05  # < 120 chars
    PEN_LONG: Final[float] = 0.02  # > 3000 chars

    BODY_SLICE: Final[int] = 400

    def __init__(self) -> None:
        self.log = get_logger("agent.knowledge.ranker")

    def rank(
        self,
        query: str,
        hits: Sequence[RetrievalHitLike],
        *,
        top_k: int = 5,
        min_score: float | None = None,
    ) -> RankResult:
        """Return hits sorted by rerank score (desc), then original score.

        Parameters
        ----------
        query: Natural-language user query.
        hits: Sequence of retrieval hits from the retriever.
        top_k: Cap the number of results returned (>0).
        min_score: Optional threshold applied to **rerank** scores.
        """

        q = (query or "").strip()
        if not q or not hits:
            return RankResult(hits=[], used_weights=self._weights_map())

        with start_span("agent.knowledge.rank", {"top_k": top_k}):
            q_tokens = _tokenize(q)
            q_phrase = q.lower()

            ranked: list[RankedHit] = []
            for h in hits:
                t = h.title or ""
                x = h.text or ""

                base = _clamp01(float(h.score))
                title_overlap = _jaccard(q_tokens, _tokenize(t))
                body_overlap = _coverage(q_tokens, _tokenize(x[: self.BODY_SLICE]))
                phrase_boost = 1.0 if _contains_phrase(q_phrase, t, x) else 0.0

                penalty = 0.0
                if len(x) < 120:
                    penalty += self.PEN_SHORT
                if len(x) > 3000:
                    penalty += self.PEN_LONG

                score = (
                    self.W_BASE * base
                    + self.W_TITLE * title_overlap
                    + self.W_BODY * body_overlap
                    + self.W_PHRASE * phrase_boost
                    - penalty
                )
                score = _clamp01(score)

                ranked.append(
                    RankedHit(
                        doc_id=h.doc_id,
                        chunk_id=h.chunk_id,
                        score=float(h.score),
                        rerank=score,
                        title=h.title,
                        text=h.text,
                        source=h.source,
                        metadata=dict(h.metadata),
                    )
                )

            # Optional threshold on rerank
            if isinstance(min_score, float):
                ranked = [h for h in ranked if h.rerank >= min_score]

            # Sort and cap
            ranked.sort(key=lambda h: (h.rerank, h.score, -len(h.text)), reverse=True)
            ranked = ranked[: max(1, int(top_k))]

            return RankResult(hits=ranked, used_weights=self._weights_map())

    # Internal ---------------------------------------------------------------
    def _weights_map(self) -> Mapping[str, float]:
        return {
            "base": self.W_BASE,
            "title": self.W_TITLE,
            "body": self.W_BODY,
            "phrase": self.W_PHRASE,
            "pen_short": self.PEN_SHORT,
            "pen_long": self.PEN_LONG,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_TOKEN_RE = re.compile(r"[\p{L}\p{N}_-]+", flags=re.IGNORECASE)

# Python's `re` lacks \p classes by default; use a pragmatic fallback
_FALLBACK_TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]+", flags=re.IGNORECASE)


def _tokenize(text: str) -> set[str]:
    if not text:
        return set()
    try:
        # If the regex engine supports Unicode properties via the `regex` module
        import regex as _rx

        return {m.group(0).lower() for m in _rx.finditer(r"[\p{L}\p{N}_-]+", text)}
    except Exception:
        return {m.group(0).lower() for m in _FALLBACK_TOKEN_RE.finditer(text)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b) or 1
    return inter / union


def _coverage(a: set[str], b: set[str]) -> float:
    if not a:
        return 0.0
    matched = len(a & b)
    return matched / len(a)


def _contains_phrase(q_phrase: str, title: str, text: str) -> bool:
    q = q_phrase.strip()
    if not q:
        return False
    tl = (title or "").lower()
    xl = (text or "").lower()
    return (q in tl) or (q in xl)


def _clamp01(x: float) -> float:
    return 0.0 if math.isnan(x) else max(0.0, min(1.0, x))
