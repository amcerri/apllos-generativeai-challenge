"""
Routing paths — end‑to‑end (supervisor rules).

Overview
--------
These tests exercise the routing supervisor's context‑first rules across common
paths (analytics, knowledge, commerce, triage) including single‑pass fallbacks.

Design
------
We avoid network/LLM calls by feeding a `RouterDecision` directly into the
supervisor and asserting the resolved `agent`. Tests are defensive and will
`pytest.skip` if the supervisor is unavailable in this environment.

Integration
-----------
Relies on `app.routing.supervisor.apply_routing_rules` and the
`app.contracts.router_decision.RouterDecision` dataclass.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from typing import Any

import pytest

apply_routing_rules: Any
try:
    import importlib

    _sup = importlib.import_module("app.routing.supervisor")
    apply_routing_rules = getattr(_sup, "apply_routing_rules", None)
except Exception:  # pragma: no cover - optional
    apply_routing_rules = None

RouterDecision: Any
try:
    from app.contracts.router_decision import RouterDecision as _RouterDecision

    RouterDecision = _RouterDecision
except Exception:  # pragma: no cover - optional
    RouterDecision = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mk_dec(**overrides: Any) -> Any:
    if RouterDecision is None:
        pytest.skip("RouterDecision contract is not available")
        raise SystemExit(0)
    base = {
        "agent": "analytics",
        "confidence": 0.9,
        "reason": "unit test seed",
        "tables": ["orders"],
        "columns": ["order_id"],
        "signals": ["allowlist:orders"],
        "thread_id": None,
    }
    base.update(overrides)
    return RouterDecision(**base)


def _as_map(x: Any) -> Mapping[str, Any]:
    if is_dataclass(x):
        return asdict(x)
    if isinstance(x, Mapping):
        return x
    # Fallback projection for objects with attributes → dict
    keys = ("agent", "confidence", "reason", "tables", "columns", "signals", "thread_id")
    return {k: getattr(x, k) for k in keys if hasattr(x, k)}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.skipif(apply_routing_rules is None, reason="supervisor not available")
def test_clear_analytics_stays_analytics() -> None:
    dec = _mk_dec(
        agent="analytics", tables=["orders"], columns=["order_id"]
    )  # clear analytics signals
    resolved = apply_routing_rules(dec)
    m = _as_map(resolved)
    assert m["agent"] == "analytics"


@pytest.mark.skipif(apply_routing_rules is None, reason="supervisor not available")
def test_knowledge_falls_back_to_analytics_when_tabular_signals_present() -> None:
    dec = _mk_dec(
        agent="knowledge",
        tables=["orders"],
        columns=["order_id"],
        signals=["allowlist:orders", "contains:order_id"],
        reason="mentions tables/columns",
    )
    resolved = apply_routing_rules(dec)
    m = _as_map(resolved)
    assert m["agent"] == "analytics"


@pytest.mark.skipif(apply_routing_rules is None, reason="supervisor not available")
def test_analytics_falls_back_to_knowledge_when_textual() -> None:
    dec = _mk_dec(
        agent="analytics",
        tables=[],
        columns=[],
        signals=["rag_hit:policy"],
        reason="textual normative question",
    )
    resolved = apply_routing_rules(dec)
    m = _as_map(resolved)
    assert m["agent"] == "knowledge"


@pytest.mark.skipif(apply_routing_rules is None, reason="supervisor not available")
def test_commerce_stays_commerce() -> None:
    dec = _mk_dec(
        agent="commerce", signals=["doc:invoice", "mime:application/pdf"], tables=[], columns=[]
    )
    resolved = apply_routing_rules(dec)
    m = _as_map(resolved)
    assert m["agent"] == "commerce"


@pytest.mark.skipif(apply_routing_rules is None, reason="supervisor not available")
def test_triage_stays_triage_when_no_context() -> None:
    dec = _mk_dec(
        agent="triage", signals=["no_context"], tables=[], columns=[], reason="insufficient context"
    )
    resolved = apply_routing_rules(dec)
    m = _as_map(resolved)
    assert m["agent"] == "triage"
