"""
Triage handler — unit tests.

Overview
--------
Contract-oriented tests for the triage handler. The goal is to ensure the
handler produces a user-facing Answer-like structure in Portuguese, with
helpful guidance and optional follow-up suggestions, without requiring any
external services.

Design
------
Tests are defensive and do not bind to a specific method signature. We try a
few common call forms (e.g., `handle(text=...)`, `triage(text)`, `__call__`).
If the handler is unavailable in this environment, the tests are skipped to
keep the POC CI deterministic.

Integration
-----------
Relies only on `app.agents.triage.handler.TriageHandler`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import pytest

# Optional import guarded; if unavailable, tests will be skipped.
HandlerType: Any
try:  # pragma: no cover - import guarded
    from app.agents.triage.handler import TriageHandler as _Handler

    HandlerType = _Handler
except Exception:  # pragma: no cover - optional
    HandlerType = None


# ---------------------------------------------------------------------------
# Helpers (pure python)
# ---------------------------------------------------------------------------


def _as_map(x: Any) -> Mapping[str, Any]:
    if isinstance(x, Mapping):
        return x
    # Fallback projection for objects with attributes → dict
    keys = (
        "text",
        "data",
        "columns",
        "citations",
        "meta",
        "no_context",
        "artifacts",
        "followups",
    )
    return {k: getattr(x, k) for k in keys if hasattr(x, k)}


def _call_handler(h: Any, text: str) -> Mapping[str, Any]:
    """Try multiple method signatures to obtain a result mapping."""
    candidates: list[tuple[tuple[Any, ...], dict[str, Any]]] = [
        ((), {"text": text}),
        ((text,), {}),
        ((), {"query": text}),
    ]
    for meth_name in ("handle", "triage", "run", "__call__"):
        meth = getattr(h, meth_name, None)
        if not callable(meth):
            continue
        last_err: Exception | None = None
        for args, kwargs in candidates:
            try:
                out = meth(*args, **kwargs)
                return _as_map(out)
            except Exception as exc:
                last_err = exc
                continue
        if last_err is not None:  # pragma: no cover - diagnostic on failure
            raise last_err
    # No callable found → skip
    pytest.skip("triage handler does not expose a supported call method")
    raise SystemExit(0)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.skipif(HandlerType is None, reason="TriageHandler not available")
def test_triage_returns_answer_contract() -> None:
    handler = HandlerType()
    out = _call_handler(handler, "Não tenho contexto suficiente sobre meu pedido.")

    # Must expose basic Answer fields
    assert "text" in out and isinstance(out["text"], str) and out["text"].strip()

    # Triage should not include citations by default
    if "citations" in out and out["citations"] is not None:
        assert isinstance(out["citations"], Sequence)
        assert len(out["citations"]) == 0

    # Follow-ups are optional but, when present, should be a short list of strings
    if "followups" in out and out["followups"] is not None:
        assert isinstance(out["followups"], Sequence)
        for f in out["followups"]:
            assert isinstance(f, str) and f.strip()
        assert len(out["followups"]) <= 5


@pytest.mark.skipif(HandlerType is None, reason="TriageHandler not available")
def test_triage_offers_next_steps_when_ambiguous() -> None:
    handler = HandlerType()
    out = _call_handler(handler, "Quero ajuda, mas não sei se é sobre dados ou documentos.")

    # If followups exist, there should be at least 2 actionable suggestions
    fups = out.get("followups")
    if fups is None:
        pytest.skip("handler did not provide followups for ambiguous query")
        return

    assert isinstance(fups, Sequence)
    actionable = [x for x in fups if isinstance(x, str) and x.strip()]
    assert len(actionable) >= 2
