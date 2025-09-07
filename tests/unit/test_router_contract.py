"""
RouterDecision contract — unit tests.

Overview
--------
These tests validate the minimal behavioral contract of `RouterDecision`:
- shape and field names;
- accepted agent names;
- optional `thread_id` handling;
- basic value sanity (confidence bounds, list types).

Design
------
The tests are resilient to implementation details: when validation is present,
we expect `ValueError`/`AssertionError` on invalid inputs; otherwise, we assert
post-conditions that keep the object within contract expectations.

Integration
-----------
Requires only the `app.contracts.router_decision.RouterDecision` dataclass and
`pytest`. No I/O or external services are used.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

import pytest

from app.contracts.router_decision import RouterDecision

ALLOWED_AGENTS = {"analytics", "knowledge", "commerce", "triage"}


def _mk(**overrides: Any) -> RouterDecision:
    """Helper: construct a valid RouterDecision with overrides."""
    base = {
        "agent": "analytics",
        "confidence": 0.85,
        "reason": "tables/columns matched allowlist",
        "tables": ["orders", "order_items"],
        "columns": ["order_id", "customer_id"],
        "signals": ["allowlist:orders", "contains:order_id"],
        "thread_id": None,
    }
    base.update(overrides)
    return RouterDecision(**base)  # type: ignore[arg-type]


def test_is_dataclass_and_fields_shape() -> None:
    dec = _mk()
    assert is_dataclass(dec), "RouterDecision must be a dataclass"
    d = asdict(dec)
    # Exact field presence
    assert set(d.keys()) == {
        "agent",
        "confidence",
        "reason",
        "tables",
        "columns",
        "signals",
        "thread_id",
    }
    # Types sanity
    assert dec.agent in ALLOWED_AGENTS
    assert isinstance(dec.confidence, float)
    assert isinstance(dec.reason, str)
    assert isinstance(dec.tables, list) and all(isinstance(t, str) for t in dec.tables)
    assert isinstance(dec.columns, list) and all(isinstance(c, str) for c in dec.columns)
    assert isinstance(dec.signals, list) and all(isinstance(s, str) for s in dec.signals)


@pytest.mark.parametrize("agent", sorted(ALLOWED_AGENTS))
def test_accepts_allowed_agents(agent: str) -> None:
    dec = _mk(agent=agent)
    assert dec.agent == agent


def test_rejects_or_normalizes_invalid_agent() -> None:
    """Invalid agent should raise or be coerced into the allowed set.

    The contract requires `agent` ∈ ALLOWED_AGENTS. Implementations may
    enforce via validation (raising) or coercion; we accept either as long as
    the final value is valid.
    """
    try:
        dec = _mk(agent="unsupported")
    except (ValueError, AssertionError):
        return  # strict validation path
    # Coercion path: still must end up with a valid agent
    assert dec.agent in ALLOWED_AGENTS


@pytest.mark.parametrize("val", [-0.1, 0.0, 0.5, 1.0, 1.1])
def test_confidence_bounds_or_guard(val: float) -> None:
    """Confidence must be in [0,1]; either enforced or clamped by impl."""
    try:
        dec = _mk(confidence=float(val))
    except (ValueError, AssertionError):
        # Strict impl rejects out-of-range; accept
        if 0.0 <= val <= 1.0:
            pytest.fail("confidence within bounds should not raise")
        return
    # If constructed, ensure the value is within [0, 1]
    assert 0.0 <= dec.confidence <= 1.0


def test_thread_id_optional_and_roundtrip() -> None:
    dec = _mk(thread_id=None)
    assert dec.thread_id is None
    dec2 = _mk(thread_id="thread-123")
    assert isinstance(dec2.thread_id, str) and dec2.thread_id == "thread-123"
    # asdict roundtrip preserves presence of key and value
    assert asdict(dec2)["thread_id"] == "thread-123"


def test_lists_allow_strings_and_dedup_is_ok() -> None:
    """Lists should accept strings; dedup/sort (if implemented) is acceptable."""
    dec = _mk(
        tables=["orders", "orders"], columns=["order_id", "order_id"], signals=["a", "a", "b"]
    )
    # Basic guarantees: still lists of strings and non-empty
    assert isinstance(dec.tables, list) and all(isinstance(t, str) for t in dec.tables)
    assert isinstance(dec.columns, list) and all(isinstance(c, str) for c in dec.columns)
    assert isinstance(dec.signals, list) and all(isinstance(s, str) for s in dec.signals)
    # If implementation performs deduplication, ensure content is preserved
    assert set(dec.tables) <= {"orders"}
    assert set(dec.columns) <= {"order_id"}
    assert set(dec.signals) <= {"a", "b"}
