"""
Routing supervisor (deterministic guards & fallbacks)

Overview
    Applies context‑first routing rules on top of the LLM router decision and
    resolves a single, final agent with at most one fallback (no loops).

Design
    - Inputs: a RouterDecision‑shaped object (dict or dataclass) and optional
      context hints (e.g., RAG hit signals).
    - Hard guards: commerce dominates when `commerce_doc` is present; never
      produce multiple fallbacks; confidence is recalibrated conservatively.
    - Output: normalized dict or RouterDecision dataclass (if available).

Integration
    - Call `supervise(decision, ctx)` from the graph after LLM classification
      and before agent dispatch.
    - Logging/tracing are optional; this module degrades gracefully without
      infra dependencies.

Usage
    >>> from app.routing.supervisor import supervise, RoutingContext
    >>> ctx = RoutingContext(rag_hits=2, rag_min_score=0.78)
    >>> final_decision = supervise({
    ...     "agent": "knowledge",
    ...     "confidence": 0.61,
    ...     "reason": "policy intent",
    ...     "tables": ["orders"],
    ...     "columns": ["order_status"],
    ...     "signals": ["mentions_table", "mentions_column"],
    ...     "thread_id": None,
    ... }, ctx)
    >>> final_decision["agent"] in {"analytics", "knowledge", "commerce", "triage"}
    True
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


# Tracing (optional; keep a single alias to avoid mypy signature clashes)
start_span: Any
try:  # Optional tracer
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attributes: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# Optional RouterDecision dataclass
ROUTER_DECISION_CLS: Any
try:
    from app.contracts.router_decision import RouterDecision as _RouterDecision

    ROUTER_DECISION_CLS = _RouterDecision
except Exception:  # pragma: no cover - optional
    ROUTER_DECISION_CLS = None

__all__ = ["RoutingContext", "supervise"]


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class RoutingContext:
    """Auxiliary signals for deterministic supervision.

    Attributes
    ----------
    rag_hits: Number of retrieved RAG chunks above threshold (0 if none).
    rag_min_score: Minimum score among used RAG chunks (None if not applicable).
    allowlist_tables: Tables detected by upstream (for convenience).
    allowlist_columns: Columns detected by upstream (for convenience).
    extra_signals: Additional signals not present in the RouterDecision.
    """

    rag_hits: int = 0
    rag_min_score: float | None = None
    allowlist_tables: tuple[str, ...] = ()
    allowlist_columns: tuple[str, ...] = ()
    extra_signals: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def supervise(decision: Mapping[str, Any] | Any, ctx: RoutingContext | None = None) -> Any:
    """Apply guardrails and single‑pass fallback to a router decision.

    Parameters
    ----------
    decision: RouterDecision‑like mapping or dataclass.
    ctx: Optional routing context with RAG and allowlist hints.

    Returns
    -------
    RouterDecision (dataclass if available; else a plain dict).
    """

    ctx = ctx or RoutingContext()

    with start_span("routing.supervise"):
        dec = _as_mapping(decision)
        agent = dec.get("agent", "triage")
        confidence = float(dec.get("confidence", 0.5) or 0.5)
        reason = str(dec.get("reason", "router output"))[:200]
        tables = list(dec.get("tables", []) or [])
        columns = list(dec.get("columns", []) or [])
        signals = set(dec.get("signals", []) or [])
        thread_id = dec.get("thread_id")

        # Merge optional context into signals for downstream observability
        if ctx.allowlist_tables:
            tables = sorted({*tables, *ctx.allowlist_tables})
        if ctx.allowlist_columns:
            columns = sorted({*columns, *ctx.allowlist_columns})
        if ctx.extra_signals:
            signals.update(ctx.extra_signals)

        # Hard guard: explicit commerce cues dominate
        if "commerce_doc" in signals:
            final = _finalize(
                dec,
                agent="commerce",
                confidence=max(confidence, 0.9),
                reason=_append_reason(reason, "commerce guard"),
                tables=tables,
                columns=columns,
                signals=sorted(signals),
                thread_id=thread_id,
            )
            return _coerce_router_decision(final)

        # Single‑pass fallback rules (context‑first)
        fallback_applied = False
        chosen = agent

        # Sync with LLMClassifier signal names: accepts both legacy and new variants.
        allowlist_cues = bool(
            tables
            or columns
            or ("sql_like" in signals)      # new structural SQL hint
            or ("sql_intent" in signals)    # legacy name
        )
        doc_cues = bool(
            ("doc_style" in signals)         # new weak document‑style hint
            or ("doc_intent" in signals)     # legacy name
            or (ctx.rag_hits and ctx.rag_hits > 0)
        )

        if agent == "analytics" and doc_cues and not allowlist_cues:
            chosen = "knowledge"
            fallback_applied = True
        elif agent == "knowledge" and allowlist_cues:
            chosen = "analytics"
            fallback_applied = True
        elif agent == "triage":
            if doc_cues:
                chosen = "knowledge"
                fallback_applied = True
            elif allowlist_cues:
                chosen = "analytics"
                fallback_applied = True

        if fallback_applied:
            # Calibrate confidence conservatively upward but capped.
            target = 0.78 if chosen in {"analytics", "knowledge"} else 0.7
            confidence = max(confidence, target)
            signals.add("supervisor_fallback")
            reason = _append_reason(reason, f"fallback→{chosen}")

        final = _finalize(
            dec,
            agent=chosen,
            confidence=confidence,
            reason=reason,
            tables=tables,
            columns=columns,
            signals=sorted(signals),
            thread_id=thread_id,
        )
        return _coerce_router_decision(final)


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _as_mapping(obj: Mapping[str, Any] | Any) -> dict[str, Any]:
    if isinstance(obj, Mapping):
        return dict(obj)
    # Dataclass or attr‑like object: try attribute access
    out: dict[str, Any] = {}
    for key in ("agent", "confidence", "reason", "tables", "columns", "signals", "thread_id"):
        if hasattr(obj, key):
            out[key] = getattr(obj, key)
    return out


def _append_reason(existing: str, extra: str) -> str:
    base = existing.strip()
    extra = extra.strip()
    if not base:
        return extra
    if not extra:
        return base
    joined = f"{base}; {extra}"
    return joined[:200]


def _finalize(
    original: Mapping[str, Any],
    *,
    agent: str,
    confidence: float,
    reason: str,
    tables: Iterable[str],
    columns: Iterable[str],
    signals: Iterable[str],
    thread_id: Any,
) -> dict[str, Any]:
    return {
        "agent": agent if agent in {"analytics", "knowledge", "commerce", "triage"} else "triage",
        "confidence": max(0.0, min(1.0, float(confidence))),
        "reason": reason[:200],
        "tables": sorted({str(t) for t in tables if str(t).strip()}),
        "columns": sorted({str(c) for c in columns if str(c).strip()}),
        "signals": sorted({str(s) for s in signals if str(s).strip()}),
        "thread_id": original.get("thread_id", thread_id),
    }


def _coerce_router_decision(dec: Mapping[str, Any]) -> Any:
    if ROUTER_DECISION_CLS is None:
        return dict(dec)
    try:
        if hasattr(ROUTER_DECISION_CLS, "from_dict"):
            return ROUTER_DECISION_CLS.from_dict(dec)
        if hasattr(ROUTER_DECISION_CLS, "from_mapping"):
            return ROUTER_DECISION_CLS.from_mapping(dec)
        return ROUTER_DECISION_CLS(**dec)
    except Exception:
        return dict(dec)
