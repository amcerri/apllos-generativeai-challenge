"""
Answer Contract

Overview
    Strict dataclass representing the user-facing response produced by any
    agent. Text is required and should be written in pt-BR by callers. Optional
    fields support tabular data (analytics), citations (knowledge), metadata,
    artifacts, and next-step suggestions.

Design
    - Stdlib-only, PEP‑8/PEP‑257 compliant.
    - Minimal runtime validation to keep results well-formed.
    - JSON Schema is provided for validation and LLM Structured Outputs.

Integration
    - Use `Answer.from_dict(...)` to build/validate from dynamic inputs.
    - For analytics, when returning rows, provide `columns` and enforce consistent
      column counts.
    - For knowledge, when using RAG, populate `citations` (at least one of
      `url` or `doc_id` per citation).

Usage
    >>> a = Answer(text="Tudo certo.")
    >>> a.to_dict()["text"]
    'Tudo certo.'
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm_columns(values: Iterable[Any] | None) -> list[str]:
    """Normalize a sequence of column names into a unique, non-empty list[str]."""

    if not values:
        return []
    out: list[str] = []
    seen = set()
    for v in values:
        s = str(v).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _norm_rows(rows: Iterable[Iterable[Any]] | None, expected_len: int | None) -> list[list[Any]]:
    """Coerce an iterable of rows into List[List[Any]] and validate lengths."""

    if rows is None:
        return []
    out: list[list[Any]] = []
    for row in rows:
        r = list(row)
        if expected_len is not None and len(r) != expected_len:
            raise ValueError(
                f"row has {len(r)} values but expected {expected_len} to match columns"
            )
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# Citation
# ---------------------------------------------------------------------------
@dataclass
class Citation:
    """Reference to a supporting source used in an answer.

    Fields
        title: short human-readable title for the source
        url: public URL (preferred when available)
        doc_id: internal document id (used for private corpora)
        chunk_id: internal chunk identifier (optional)
        lines: human-readable line range (e.g., "L10-L20")

    At least one of `url` or `doc_id` must be provided by callers.
    """

    title: str
    url: str | None = None
    doc_id: str | None = None
    chunk_id: str | None = None
    lines: str | None = None

    def __post_init__(self) -> None:
        t = (self.title or "").strip()
        if not t:
            raise ValueError("citation.title must be a non-empty string")
        self.title = t
        if self.url is not None:
            self.url = self.url.strip() or None
        if self.doc_id is not None:
            self.doc_id = self.doc_id.strip() or None
        if self.chunk_id is not None:
            self.chunk_id = self.chunk_id.strip() or None
        if self.lines is not None:
            self.lines = self.lines.strip() or None
        if not (self.url or self.doc_id):
            raise ValueError("citation must contain either 'url' or 'doc_id'")

    def to_dict(self) -> dict[str, Any]:  # JSON-serializable
        return {
            "title": self.title,
            "url": self.url,
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id,
            "lines": self.lines,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Citation:
        if not isinstance(data, Mapping):
            raise ValueError("citation data must be a mapping")
        title = data.get("title")
        url = data.get("url")
        doc_id = data.get("doc_id")
        chunk_id = data.get("chunk_id")
        lines = data.get("lines")
        if title is None:
            raise ValueError("citation missing required field 'title'")
        return cls(title=str(title), url=url, doc_id=doc_id, chunk_id=chunk_id, lines=lines)


# ---------------------------------------------------------------------------
# Answer
# ---------------------------------------------------------------------------
@dataclass
class Answer:
    """Agent answer contract with minimal runtime validation.

    Fields
        text: user-facing message (pt-BR). Required.
        data: optional table rows (list of rows); used by analytics agent.
        columns: optional list of column names; required when `data` is provided.
        citations: optional list of `Citation`; required by knowledge agent when RAG is used.
        meta: free-form metadata (e.g., sql, row_count, timings, limit_applied).
        no_context: for knowledge agent; true when retrieval was weak/empty.
        artifacts: arbitrary structured artifacts (e.g., email draft).
        followups: actionable next-step suggestions for the user.
    """

    text: str
    data: list[list[Any]] | None = None
    columns: list[str] | None = None
    citations: list[Citation] | None = None
    meta: dict[str, Any] | None = None
    no_context: bool | None = None
    artifacts: dict[str, Any] | None = None
    followups: list[str] | None = None

    # ---------------------------
    # Validation & normalization
    # ---------------------------
    def __post_init__(self) -> None:
        # text
        t = (self.text or "").strip()
        if not t:
            raise ValueError("text must be a non-empty string")
        self.text = t

        # columns normalization
        cols = _norm_columns(self.columns)
        self.columns = cols or (None if self.data in (None, []) else [])

        # data normalization and shape checks
        if self.data is not None:
            if self.columns is None:
                raise ValueError("columns must be provided when data is present")
            expected_len = len(self.columns)
            self.data = _norm_rows(self.data, expected_len)

        # citations normalization
        if self.citations is not None:
            norm: list[Citation] = []
            for c in self.citations:
                if isinstance(c, Mapping):
                    norm.append(Citation.from_dict(c))
                elif isinstance(c, Citation):
                    norm.append(c)
                else:
                    raise ValueError("citations must be Citation or mapping")
            self.citations = norm

        # followups normalization
        if self.followups is not None:
            self.followups = [s for s in (str(x).strip() for x in self.followups) if s]
            if not self.followups:
                self.followups = None

    # ---------------------------
    # Conversions
    # ---------------------------
    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "text": self.text,
            "data": self.data,
            "columns": self.columns,
            "meta": self.meta,
            "no_context": self.no_context,
            "artifacts": self.artifacts,
            "followups": self.followups,
        }
        if self.citations is not None:
            out["citations"] = [c.to_dict() for c in self.citations]
        return out

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Answer:
        if not isinstance(data, Mapping):
            raise ValueError("data must be a mapping")
        try:
            text_raw = data["text"]
        except KeyError as exc:
            raise ValueError("missing required field: text") from exc

        rows = data.get("data")
        columns = data.get("columns")
        citations_in = data.get("citations")

        citations_parsed: list[Citation] | None = None
        if citations_in is not None:
            if not isinstance(citations_in, Iterable):
                raise ValueError("citations must be a list-like of objects")
            tmp: list[Citation] = []
            for c in citations_in:
                if isinstance(c, Mapping):
                    tmp.append(Citation.from_dict(c))
                elif isinstance(c, Citation):
                    tmp.append(c)
                else:
                    raise ValueError("citations must be Citation or mapping")
            citations_parsed = tmp

        # Normalize rows into a list of lists if an iterable is provided
        rows_out: list[list[Any]] | None = None
        if isinstance(rows, Iterable):
            try:
                rows_out = [list(r) for r in rows]
            except TypeError:
                rows_out = None

        cols_out: list[str] | None = None
        if isinstance(columns, Iterable):
            cols_out = [str(c).strip() for c in columns]

        meta_val = data.get("meta")
        meta_dict: dict[str, Any] | None = dict(meta_val) if isinstance(meta_val, Mapping) else None

        artifacts_val = data.get("artifacts")
        artifacts_dict: dict[str, Any] | None = (
            dict(artifacts_val) if isinstance(artifacts_val, Mapping) else None
        )

        followups_val = data.get("followups", None)
        followups_list: list[str] | None = (
            [str(f) for f in followups_val] if isinstance(followups_val, Iterable) else None
        )

        no_context_val = None
        if "no_context" in data:
            no_context_val = bool(data.get("no_context"))

        return cls(
            text=str(text_raw),
            data=rows_out,
            columns=cols_out,
            citations=citations_parsed,
            meta=meta_dict,
            no_context=no_context_val,
            artifacts=artifacts_dict,
            followups=followups_list,
        )

    # ---------------------------
    # JSON Schema for Structured Outputs
    # ---------------------------
    JSON_SCHEMA: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Answer",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "text": {"type": "string", "minLength": 1},
            "data": {"type": ["array", "null"], "items": {"type": "array"}},
            "columns": {"type": ["array", "null"], "items": {"type": "string"}},
            "citations": {
                "type": ["array", "null"],
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "title": {"type": "string", "minLength": 1},
                        "url": {"type": ["string", "null"]},
                        "doc_id": {"type": ["string", "null"]},
                        "chunk_id": {"type": ["string", "null"]},
                        "lines": {"type": ["string", "null"]},
                    },
                    "required": ["title"],
                    "anyOf": [
                        {"required": ["url"]},
                        {"required": ["doc_id"]},
                    ],
                },
            },
            "meta": {"type": ["object", "null"]},
            "no_context": {"type": ["boolean", "null"]},
            "artifacts": {"type": ["object", "null"]},
            "followups": {"type": ["array", "null"], "items": {"type": "string"}},
        },
        "required": ["text"],
    }

    @classmethod
    def schema(cls) -> dict[str, Any]:
        """Return a (shallow) copy of the JSON Schema dict."""

        return dict(cls.JSON_SCHEMA)
