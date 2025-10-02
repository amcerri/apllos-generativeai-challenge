"""
Ingest documents into pgvector (RAG index).

Overview
--------
Chunk and embed PDF/TXT/MD documents from a directory and upsert the vectors
into PostgreSQL using the pgvector extension. The script is dependency‑light
and degrades gracefully when optional libs (OpenAI, PyPDF) are missing.

Design
------
1) Create schema/table if needed (idempotent). Ensure `vector` extension.
2) Discover files by glob pattern (default: *.pdf, *.txt, *.md).
3) Extract text (PyPDF if present; otherwise skip PDFs) and chunk by characters.
4) Generate embeddings via OpenAI (if available) or a deterministic fallback.
5) Upsert (doc_id, chunk_id) rows with `embedding vector(dim)` and metadata.
6) Build/refresh ANN index (HNSW/IVFFlat) only when necessary.

Integration
-----------
- Reads `DATABASE_URL` unless `app.infra.db.get_engine()` is available.
- Embeddings: `OPENAI_API_KEY` + `EMBEDDING_MODEL` (default: text-embedding-3-small).
- Table configurable via env `RAG_TABLE` (default: `rag.chunks`).

Usage
-----
$ python -m scripts.ingest_vectors \
    --docs-dir data/docs \
    --pattern "*.pdf,*.txt,*.md" \
    --max-chars 1200 --overlap 150 \
    --dim 1536 --index-method hnsw --rebuild-index
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional infra: logging & tracing with fallbacks
# ---------------------------------------------------------------------------
try:
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - simple fallback
        return _logging.getLogger(component)


start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# ---------------------------------------------------------------------------
# Optional libs: SQLAlchemy, OpenAI, PyPDF
# ---------------------------------------------------------------------------
_get_engine: Any = None

Engine: Any
try:
    from sqlalchemy import create_engine as _create_engine
    from sqlalchemy.engine import Engine as _Engine

    Engine = _Engine
except Exception:  # pragma: no cover - optional
    Engine = object  # sentinel type

try:
    from app.infra.db import get_engine as _get_engine
except Exception:  # pragma: no cover - optional
    pass

OpenAIClient: Any = None
try:  # OpenAI SDK v1 style
    from openai import OpenAI as _OpenAIClient

    OpenAIClient = _OpenAIClient
except Exception:  # pragma: no cover - optional
    try:  # Legacy SDK
        import openai as _openai

        OpenAIClient = _openai
    except Exception:  # pragma: no cover - optional
        OpenAIClient = None

PdfReader: Any = None
try:
    from pypdf import PdfReader as _PdfReader  # light, pure‑python

    PdfReader = _PdfReader
except Exception:  # pragma: no cover - optional
    PdfReader = None

# ---------------------------------------------------------------------------
# Constants & dataclasses
# ---------------------------------------------------------------------------
_DEFAULT_DOCS_DIR: Final[str] = "data/docs"
_DEFAULT_PATTERN: Final[str] = "*.pdf,*.txt,*.md"
_DEFAULT_MODEL: Final[str] = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
_DEFAULT_DIM: Final[int] = int(os.environ.get("EMBEDDING_DIM", "1536"))
_DEFAULT_TABLE: Final[str] = os.environ.get("RAG_TABLE", "public.doc_chunks")

_TRUE: Final[set[str]] = {"1", "true", "yes", "on"}


@dataclass(slots=True)
class IngestOpts:
    docs_dir: Path
    patterns: list[str]
    max_chars: int
    overlap: int
    model: str
    dim: int
    index_method: str  # "hnsw" | "ivfflat"
    rebuild_index: bool
    limit: int | None


# ---------------------------------------------------------------------------
# Engine helpers
# ---------------------------------------------------------------------------


def _resolve_engine() -> Any:
    if _get_engine is not None:
        try:
            return _get_engine()
        except RuntimeError:
            # Fall back to DATABASE_URL if infra engine is not configured
            pass
    
    if globals().get("_create_engine") is None:
        raise RuntimeError("SQLAlchemy is required but not available")
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set and infra.get_engine is unavailable")
    return _create_engine(url, pool_pre_ping=True, future=True)


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf_text(path: Path) -> str:
    if PdfReader is None:
        return ""  # graceful: no PDF support installed
    try:
        reader = PdfReader(str(path))
        texts: list[str] = []
        for page in reader.pages:
            try:
                texts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(t for t in texts if t)
    except Exception:
        return ""


def load_text(path: Path) -> tuple[str, str]:
    """Return (title, text) from file path; empty text if unsupported."""
    name = path.stem
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return name, _read_text_file(path)
    if suffix == ".pdf":
        return name, _read_pdf_text(path)
    return name, ""


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------


def chunk_text(text: str, *, max_chars: int, overlap: int) -> list[str]:
    """Character window chunking with overlap (robust to missing tokenizers)."""
    text = (text or "").strip()
    if not text:
        return []
    max_chars = max(100, int(max_chars))
    overlap = max(0, min(int(overlap), max_chars // 2))
    chunks: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        j = min(n, i + max_chars)
        chunk = text[i:j]
        chunks.append(chunk)
        if j >= n:
            break
        i = j - overlap
    return chunks


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------


def _openai_embed(texts: Sequence[str], *, model: str) -> list[list[float]]:
    if OpenAIClient is None:
        raise RuntimeError("OpenAI SDK not available")

    # New SDK (client = OpenAI())
    if hasattr(OpenAIClient, "Embeddings") or hasattr(OpenAIClient, "OpenAI"):
        try:
            client = OpenAIClient() if callable(OpenAIClient) else OpenAIClient
            resp = client.embeddings.create(model=model, input=list(texts))
            return [list(d.embedding) for d in resp.data]
        except Exception as exc:  # fall back below
            raise RuntimeError(f"openai embedding failed: {type(exc).__name__}") from exc

    # Legacy SDK style (openai.Embedding.create)
    if hasattr(OpenAIClient, "Embedding"):
        try:
            resp = OpenAIClient.Embedding.create(model=model, input=list(texts))
            return [list(d["embedding"]) for d in resp["data"]]
        except Exception as exc:  # fall back below
            raise RuntimeError(f"openai embedding failed: {type(exc).__name__}") from exc

    raise RuntimeError("Unsupported OpenAI client")


def _fallback_embed(texts: Sequence[str], *, dim: int) -> list[list[float]]:
    """Deterministic hash‑based embedding; useful for tests without network."""
    out: list[list[float]] = []
    for t in texts:
        h = hashlib.sha256((t or "").encode("utf-8")).digest()
        # Expand to dim by repeating hash; map bytes to floats in [0,1)
        vec = [(h[i % len(h)] / 255.0) for i in range(dim)]
        out.append(vec)
    return out


def embed_texts(texts: Sequence[str], *, model: str, dim: int) -> list[list[float]]:
    try:
        return _openai_embed(texts, model=model)
    except Exception:
        return _fallback_embed(texts, dim=dim)


# ---------------------------------------------------------------------------
# Database DDL/DML
# ---------------------------------------------------------------------------


def _ensure_schema(engine: Any, *, dim: int, table: str) -> None:
    schema, _, name = table.partition(".")
    schema = schema or "public"
    name = name or table
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector")
        conn.exec_driver_sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        conn.exec_driver_sql(
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.{name} (
                id         SERIAL PRIMARY KEY,
                doc_id     TEXT,
                chunk_id   TEXT,
                title      TEXT,
                content    TEXT NOT NULL,
                embedding  vector({dim}),
                source     TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                metadata   JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _index_exists(engine: Any, *, table: str) -> bool:
    schema, _, name = table.partition(".")
    schema = schema or "public"
    name = name or table
    q = (
        "SELECT 1 FROM pg_indexes WHERE schemaname = %(schema)s AND indexname = %(idx)s LIMIT 1"
    )
    idx_name = f"idx_{name}_embedding"
    params = {"schema": schema, "idx": idx_name}
    with engine.begin() as conn:
        res = conn.exec_driver_sql(q, params)
        row = res.first()
        return bool(row)


def _create_index(engine: Any, *, table: str, method: str) -> None:
    schema, _, name = table.partition(".")
    schema = schema or "public"
    name = name or table
    method = method.lower()
    idx_name = f"idx_{name}_embedding"
    if method not in {"hnsw", "ivfflat"}:
        method = "hnsw"
    with engine.begin() as conn:
        # Drop and recreate if method has changed (best effort)
        conn.exec_driver_sql(f"DROP INDEX IF EXISTS {schema}.{idx_name}")
        if method == "hnsw":
            conn.exec_driver_sql(
                f"CREATE INDEX {idx_name} ON {schema}.{name} USING hnsw (embedding vector_cosine_ops)"
            )
        else:
            conn.exec_driver_sql(
                f"CREATE INDEX {idx_name} ON {schema}.{name} USING ivfflat (embedding vector_cosine_ops) WITH (lists=100)"
            )


def upsert_chunks(
    engine: Any,
    *,
    table: str,
    doc_id: str,
    title: str,
    source_path: str,
    chunks: Sequence[str],
    embeddings: Sequence[Sequence[float]],
) -> int:
    schema, _, name = table.partition(".")
    schema = schema or "public"
    name = name or table

    rows = []
    for i, (content, emb) in enumerate(zip(chunks, embeddings, strict=False)):
        rows.append(
            {
                "doc_id": doc_id,
                "chunk_id": f"chunk_{i}",
                "title": title,
                "content": content,
                "embedding": emb,
                "source": source_path,
                "chunk_index": i,
                "metadata": json.dumps({}),
            }
        )

    if not rows:
        return 0

    cols = [
        "doc_id",
        "chunk_id",
        "title",
        "content",
        "embedding",
        "source",
        "chunk_index",
        "metadata",
    ]
    placeholders = ", ".join([f"%({c})s" for c in cols])

    # Use a single-row VALUES; passing a list of dicts to exec_driver_sql triggers
    # executemany() under the hood. This avoids building a huge multi-VALUES string
    # and works reliably across DBAPI drivers/paramstyles.
    sql = (
        f"INSERT INTO {schema}.{name} (" + ", ".join(cols) + ") VALUES (" + placeholders + ")"
    )

    with engine.begin() as conn:
        conn.exec_driver_sql(sql, rows)
        return len(rows)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def discover_files(base: Path, patterns: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for pat in patterns:
        files.extend(sorted(base.rglob(pat)))
    return files


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> IngestOpts:
    ap = argparse.ArgumentParser(description="Ingest docs into pgvector")
    ap.add_argument("--docs-dir", default=_DEFAULT_DOCS_DIR, type=Path)
    ap.add_argument(
        "--pattern",
        default=_DEFAULT_PATTERN,
        type=str,
        help="Comma‑separated glob(s), e.g. '*.pdf,*.txt'",
    )
    ap.add_argument("--max-chars", default=1200, type=int)
    ap.add_argument("--overlap", default=150, type=int)
    ap.add_argument("--model", default=_DEFAULT_MODEL, type=str)
    ap.add_argument("--dim", default=_DEFAULT_DIM, type=int)
    ap.add_argument("--index-method", default="hnsw", choices=["hnsw", "ivfflat"], type=str)
    ap.add_argument("--rebuild-index", action="store_true")
    ap.add_argument("--limit", default=None, type=int)
    ns = ap.parse_args(argv)
    patterns = [p.strip() for p in ns.pattern.split(",") if p.strip()]
    return IngestOpts(
        docs_dir=ns.docs_dir,
        patterns=patterns,
        max_chars=ns.max_chars,
        overlap=ns.overlap,
        model=ns.model,
        dim=ns.dim,
        index_method=ns.index_method,
        rebuild_index=bool(ns.rebuild_index),
        limit=ns.limit,
    )


def main(argv: list[str] | None = None) -> int:
    log = get_logger("scripts.ingest_vectors")
    opts = parse_args(argv)
    engine = _resolve_engine()

    _ensure_schema(engine, dim=opts.dim, table=_DEFAULT_TABLE)

    files = discover_files(opts.docs_dir, opts.patterns)
    if opts.limit is not None:
        files = files[: max(0, int(opts.limit))]

    if not files:
        log.warning("no files matched", dir=str(opts.docs_dir), patterns=opts.patterns)
        return 0

    total_chunks = 0
    with start_span("vectors.ingest", {"files": len(files)}):
        for path in files:
            title, text = load_text(path)
            if not text.strip():
                log.info("skip empty/unsupported file", path=str(path))
                continue

            chunks = chunk_text(text, max_chars=opts.max_chars, overlap=opts.overlap)
            if not chunks:
                continue

            embeddings = embed_texts(chunks, model=opts.model, dim=opts.dim)

            # doc_id based on relative path and mtime for stable updates
            rel = path.as_posix()
            st = path.stat()
            doc_id = hashlib.sha1(f"{rel}:{st.st_mtime_ns}".encode()).hexdigest()

            total_chunks += upsert_chunks(
                engine,
                table=_DEFAULT_TABLE,
                doc_id=doc_id,
                title=title,
                source_path=rel,
                chunks=chunks,
                embeddings=embeddings,
            )

    # Index management
    if opts.rebuild_index or not _index_exists(engine, table=_DEFAULT_TABLE):
        _create_index(engine, table=_DEFAULT_TABLE, method=opts.index_method)

    # ANALYZE for planner stats
    schema, _, name = _DEFAULT_TABLE.partition(".")
    schema = schema or "public"
    name = name or _DEFAULT_TABLE
    with engine.begin() as conn:
        conn.exec_driver_sql(f"ANALYZE {schema}.{name}")

    log.info("ingest complete", files=len(files), chunks=total_chunks)
    return 0


if __name__ == "__main__":  # pragma: no cover - manual exec
    raise SystemExit(main())
