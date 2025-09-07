"""
Knowledge retrieval — unit tests (retriever behavior).

Overview
--------
Property-based checks for the Knowledge retriever. We validate the minimal
contract without binding to implementation details or specific backends.

What we assert:
- `retrieve()` returns a finite sequence (<= k) of hits;
- each hit exposes at least a `score` (float) and is mapping-like;
- scores are non-increasing (sorted by relevance);
- an optional `min_score` filters results (if backend supports it).

Design
------
These tests are defensive: if the retriever cannot initialize (e.g. missing
DB/pgvector) or requires network, we `pytest.skip` gracefully to keep CI
stable for this POC.

Integration
-----------
Relies only on `app.agents.knowledge.retriever.KnowledgeRetriever` and the
`settings` fixture (for `retrieval_min_score`).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import pytest

# Optional import: if not present or fails, tests skip
RetrieverType: Any
try:  # pragma: no cover - import guarded
    from app.agents.knowledge.retriever import KnowledgeRetriever as _Retriever

    RetrieverType = _Retriever
except Exception:  # pragma: no cover - optional
    RetrieverType = None


@pytest.mark.skipif(RetrieverType is None, reason="KnowledgeRetriever not available")
def test_retrieve_basic_contract(settings: Mapping[str, Any]) -> None:
    retriever = RetrieverType()
    try:
        hits = retriever.retrieve(
            query="o que é e-commerce?",
            k=5,
            min_score=float(settings.get("retrieval_min_score", 0.2)),
            filters=None,
        )
    except Exception as exc:  # e.g., no DB/pgvector — skip in this POC
        pytest.skip(f"retriever unavailable: {type(exc).__name__}")
        return

    assert isinstance(hits, Sequence), "retrieve() must return a sequence"
    assert len(hits) <= 5, "must respect k upper bound"

    if not hits:  # acceptable in empty index
        return

    # Each hit should be mapping-like and carry a numeric score
    def _as_map(x: Any) -> Mapping[str, Any]:
        if isinstance(x, Mapping):
            return x
        # dataclass or object with attrs — best effort
        keys = ("score", "doc_id", "url", "chunk_id", "title", "text")
        return {k: getattr(x, k) for k in keys if hasattr(x, k)}

    ms = float(settings.get("retrieval_min_score", 0.2))
    scores: list[float] = []
    for h in hits:
        m = _as_map(h)
        assert "score" in m, "hit must expose a score"
        assert isinstance(m["score"], int | float), "score must be numeric"
        s = float(m["score"])  # normalize
        scores.append(s)
        assert 0.0 <= s <= 1.0, "score should be within [0, 1]"
        # If backend applied min_score, ensure it is respected (allow slight slack)
        assert s + 1e-9 >= ms or ms <= 0.0

    # Non-increasing order (sorted by relevance)
    assert all(scores[i] >= scores[i + 1] - 1e-12 for i in range(len(scores) - 1))


@pytest.mark.skipif(RetrieverType is None, reason="KnowledgeRetriever not available")
def test_respects_k_and_min_score(settings: Mapping[str, Any]) -> None:
    retriever = RetrieverType()

    # Use a high threshold to likely get 0..few results, but allow empty
    hi = max(0.0, min(1.0, float(settings.get("retrieval_min_score", 0.2)) + 0.6))

    try:
        hits = retriever.retrieve(query="guides", k=3, min_score=hi, filters=None)
    except Exception as exc:
        pytest.skip(f"retriever unavailable: {type(exc).__name__}")
        return

    assert isinstance(hits, Sequence)
    assert len(hits) <= 3

    # If any results survive the filter, they must meet the threshold
    for h in hits:
        m = h if isinstance(h, Mapping) else {"score": getattr(h, "score", 0.0)}
        assert float(m.get("score", 0.0)) + 1e-9 >= hi
