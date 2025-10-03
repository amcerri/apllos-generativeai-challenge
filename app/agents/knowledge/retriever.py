"""
Knowledge retriever (pgvector + embeddings).

Overview
--------
Retrieve the most relevant document chunks from a Postgres/pgvector store given a
natural‑language query. The retriever computes a query embedding (OpenAI by
default, with a deterministic local fallback), performs a vector search with
optional metadata filters, applies a minimum similarity threshold, and returns a
small, deduplicated set of hits for ranking/answering.

Design
------
- Storage: table of chunks with columns (suggested):
  `doc_id TEXT, chunk_id TEXT, title TEXT, content TEXT, source TEXT,
   metadata JSONB, embedding VECTOR` (cosine distance index).
- Query: `ORDER BY embedding <=> :qvec` (cosine distance); similarity is
  `1 - (embedding <=> :qvec)` assuming normalized vectors.
- Filtering: lightweight SQL WHERE clauses for common fields (doc_id, source,
  title, mime, tag); for generic key/value, uses JSON containment on metadata.
- Deduplication: keep the best chunk per `doc_id` by score.
- Safety: no DML/DDL; parameterized SQL; no untrusted string interpolation.

Integration
-----------
- Used by the `knowledge` agent prior to ranking/answering. Typical call:

>>> from app.agents.knowledge.retriever import KnowledgeRetriever
>>> retr = KnowledgeRetriever()
>>> out = retr.retrieve("política de devolução Olist", top_k=6, min_score=0.62)
>>> out.no_context in (True, False)
True

Usage
-----
Set `OPENAI_API_KEY` to enable OpenAI embeddings. Without it, the retriever
falls back to a deterministic local hasher (sufficient for tests, not for prod).
"""

from __future__ import annotations

import json
import os
import re
import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from time import monotonic
from typing import Any, Final

import sqlalchemy as sa
from sqlalchemy.engine import Engine

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:  # Optional config
    from app.config import get_config
except Exception:  # pragma: no cover - optional
    def get_config():
        return None


# Tracing (optional; single alias to avoid mypy signature clashes)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

__all__ = ["RetrievalHit", "RetrievalResult", "KnowledgeRetriever"]


# ---------------------------------------------------------------------------
# Result contracts
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class RetrievalHit:
    """Single retrieved chunk with similarity score and payload."""

    doc_id: str
    chunk_id: str
    score: float
    title: str | None
    text: str
    source: str | None
    metadata: dict[str, Any]


@dataclass(slots=True)
class RetrievalResult:
    """Retrieval outcome with diagnostics."""

    hits: list[RetrievalHit]
    elapsed_ms: float
    used_filters: dict[str, Any]
    no_context: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "hits": [hit.__dict__ for hit in self.hits],
            "elapsed_ms": self.elapsed_ms,
            "used_filters": dict(self.used_filters),
            "no_context": self.no_context,
        }


# ---------------------------------------------------------------------------
# Retriever
# ---------------------------------------------------------------------------
class KnowledgeRetriever:
    """Embedding‑based retriever over pgvector.

    Parameters
    ----------
    table: Name of the chunk table (default: "doc_chunks").
    model: Embedding model id (default: "text-embedding-3-small").
    distance: Vector distance (currently only "cosine" supported).
    candidate_factor: Fetch this many times `top_k` before deduplication.
    """

    DEFAULT_TABLE: Final[str] = "doc_chunks"
    DEFAULT_MODEL: Final[str] = "text-embedding-3-small"

    def __init__(
        self,
        *,
        table: str | None = None,
        model: str | None = None,
        distance: str = "cosine",
        candidate_factor: int = 4,
    ) -> None:
        self.log = get_logger("agent.knowledge.retriever")
        self._config = get_config()
        
        # Get configuration values with fallbacks
        if self._config is None:
            default_table = self.DEFAULT_TABLE
            default_model = self.DEFAULT_MODEL
        else:
            retrieval_config = self._config.get_knowledge_retrieval_config()
            default_table = retrieval_config.get("index", self.DEFAULT_TABLE)
            default_model = self._config.get_llm_model("embeddings")
        
        self.table = _validate_table_name(table or default_table)
        self.model = model or default_model
        self.distance = distance
        self.candidate_factor = max(1, int(candidate_factor))

    # Public API -------------------------------------------------------------
    def retrieve(
        self,
        query: str,
        *,
        top_k: int | None = None,
        min_score: float | None = None,
        filters: Mapping[str, Any] | None = None,
    ) -> RetrievalResult:
        """Return top‑K hits above `min_score` with light deduplication.

        If there are zero hits ≥ `min_score`, `no_context` will be True.
        """
        
        # Get configuration values with fallbacks
        if self._config is None:
            default_top_k = 5
            default_min_score = 0.6
        else:
            retrieval_config = self._config.get_knowledge_retrieval_config()
            default_top_k = retrieval_config.get("top_k", 5)
            default_min_score = retrieval_config.get("min_score", 0.6)

        top_k_i = max(1, int(top_k or default_top_k))
        min_score_f = min(1.0, max(0.0, float(min_score or default_min_score)))

        if not (query or "").strip():
            return RetrievalResult(hits=[], elapsed_ms=0.0, used_filters={}, no_context=True)

        with start_span("agent.knowledge.retrieve", {"top_k": top_k_i, "min_score": min_score_f}):
            t0 = monotonic()
            qvec = _embed_query(query, model=self.model)
            engine = _get_engine()

            limit = max(1, top_k_i * self.candidate_factor)
            where_sql, where_params = _build_where(filters or {})

            if self.distance != "cosine":
                raise ValueError("only cosine distance is supported in this POC")

            # Similarity: 1 - cosine_distance (assuming normalized vectors)
            sql = (
                f"SELECT doc_id, chunk_id, title, content, source, metadata, "
                f"(1 - (embedding <=> CAST(:qvec AS vector))) AS score "
                f"FROM {self.table} {where_sql} "
                f"ORDER BY embedding <=> CAST(:qvec AS vector) ASC "
                f"LIMIT :limit"
            )

            params: dict[str, Any] = {"qvec": qvec, "limit": limit, **where_params}
            rows = _execute(engine, sql, params)

            hits = [
                RetrievalHit(
                    doc_id=str(r.get("doc_id", "")),
                    chunk_id=str(r.get("chunk_id", "")),
                    score=float(r.get("score", 0.0) or 0.0),
                    title=str(r.get("title")) if r.get("title") is not None else None,
                    text=str(r.get("content", "")),
                    source=str(r.get("source")) if r.get("source") is not None else None,
                    metadata=_coerce_json(r.get("metadata")),
                )
                for r in rows
            ]

            # Deduplicate by doc_id keeping best score
            dedup: dict[str, RetrievalHit] = {}
            for h in hits:
                if h.doc_id not in dedup or h.score > dedup[h.doc_id].score:
                    dedup[h.doc_id] = h

            hits2 = sorted(dedup.values(), key=lambda h: h.score, reverse=True)
            hits2 = [h for h in hits2 if h.score >= min_score_f]
            hits2 = hits2[: top_k_i]

            elapsed = (monotonic() - t0) * 1000.0
            return RetrievalResult(
                hits=hits2,
                elapsed_ms=elapsed,
                used_filters=dict(filters or {}),
                no_context=(len(hits2) == 0),
            )


# ---------------------------------------------------------------------------
# DB / Embeddings / Filters helpers
# ---------------------------------------------------------------------------

_TABLE_RE = re.compile(r"^[A-Za-z_][\w]*(\.[A-Za-z_][\w]*)?$")

def _validate_table_name(name: str) -> str:
    """
    Ensure the table identifier is safe for interpolation in a raw SQL text.

    Accepts simple identifiers or schema-qualified names (schema.table).
    """
    if not _TABLE_RE.match(name):
        raise ValueError("invalid table name")
    return name


def _get_engine() -> Engine:
    try:
        from app.infra.db import get_engine  # local import keeps optional dep
    except Exception as exc:  # pragma: no cover - optional
        raise RuntimeError("database engine accessor not available") from exc
    return get_engine()


def _execute(engine: Engine, sql: str, params: Mapping[str, Any]) -> list[dict[str, Any]]:
    with engine.connect() as conn:
        result = conn.execute(sa.text(sql), params)
        return [dict(r) for r in result.mappings()]


def _embed_query(text: str, *, model: str) -> Sequence[float]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            from openai import OpenAI  # lazy import

            client = OpenAI()
            resp = client.embeddings.create(model=model, input=text)
            vec = resp.data[0].embedding
            # Ensure a plain list[float]
            return [float(x) for x in vec]
        except Exception:
            # Fall through to local hasher
            pass
    # Deterministic local fallback (bag-of-words hash into 256 dims)
    return _hash_embed(text)


def _hash_embed(text: str, *, dim: int = 1536) -> list[float]:
    vec = [0.0] * dim
    for tok in re.findall(r"[\w\-]+", text.lower()):
        d = hashlib.sha256(tok.encode("utf-8")).digest()
        idx = int.from_bytes(d[:4], "big") % dim
        vec[idx] += 1.0
    norm2 = (sum(v * v for v in vec) ** 0.5) or 1.0
    return [v / norm2 for v in vec]


def _build_where(filters: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    if not filters:
        return "", {}
    clauses: list[str] = []
    params: dict[str, Any] = {}

    if doc := filters.get("doc_id"):
        clauses.append("doc_id = :doc_id")
        params["doc_id"] = str(doc)
    if src := filters.get("source"):
        clauses.append("source = :source")
        params["source"] = str(src)
    if title := filters.get("title"):
        clauses.append("title ILIKE :title")
        params["title"] = f"%{title}%"
    if mime := filters.get("mime"):
        clauses.append("(metadata ->> 'mime') = :mime")
        params["mime"] = str(mime)
    if tag := filters.get("tag"):
        clauses.append("(metadata -> 'tags') ? :tag")
        params["tag"] = str(tag)

    # Generic metadata filter: expects dict[str, Any]; use JSONB containment
    if meta := filters.get("metadata"):
        clauses.append("metadata @> :meta")
        params["meta"] = json.dumps(meta)

    where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where_sql, params


def _coerce_json(v: Any) -> dict[str, Any]:
    if v is None:
        return {}
    if isinstance(v, dict):
        # ensure dict[str, Any]
        return {str(k): v[k] for k in v.keys()}
    try:
        return json.loads(v) if isinstance(v, str) else dict(v)
    except Exception:
        return {}
