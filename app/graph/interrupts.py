"""
Human-in-the-loop interrupts (LangGraph-friendly helpers).

Overview
--------
Provide lightweight, dependency-free helpers to declare **human approval gates**
that can be emitted by graph nodes (e.g., before executing SQL or calling
external services). The resulting payloads are plain dictionaries suitable for
transport and storage by a checkpointer.

Design
------
- `HumanGate` and `HumanResponse` dataclasses model the request/response shape.
- Factory helpers for common gates: SQL execution and external API call.
- Safe serialization: details are coerced to JSON-serializable primitives.
- Optional logging/tracing via the shared infra (fallbacks provided).

Integration
-----------
Typical usage inside a node (pseudocode):

>>> from app.graph.interrupts import make_sql_gate
>>> interrupt = make_sql_gate(
...     sql="SELECT count(*) FROM orders WHERE status = :status LIMIT 100",
...     params={"status": "delivered"},
...     limit=100,
...     tables=["orders"],
...     reason="Confirm SQL execution in production",
... )
>>> # Return/yield `interrupt` to pause the graph and await human input.

When resuming, feed a mapping like `{ "approved": true, "comment": "ok" }`
into the awaiting node and parse it with `parse_human_response`.

Usage
-----
These helpers do not depend on LangGraph directly; they only shape payloads. The
LangGraph Server/Studio can render the `type`, `name`, `title`, `message` and
`details` fields, and a checkpointer can store/restore them.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Final, Literal, Callable
from contextlib import AbstractContextManager, nullcontext as _nullcontext

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


# Tracing (optional; single alias)
start_span: Callable[[str, dict[str, Any] | None], AbstractContextManager[Any]]
try:
    from app.infra.tracing import start_span as _start_span
    start_span = _start_span
except Exception:  # pragma: no cover - optional
    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None) -> AbstractContextManager[Any]:
        return _nullcontext()
    start_span = _fallback_start_span

__all__ = [
    "HumanGate",
    "HumanResponse",
    "make_interrupt",
    "parse_human_response",
    "make_sql_gate",
    "make_external_call_gate",
    "GATE_SQL_EXECUTION",
    "GATE_EXTERNAL_CALL",
]


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class HumanGate:
    """Human approval request emitted by a graph node."""

    name: str
    title: str
    message: str
    severity: Literal["low", "medium", "high"] = "medium"
    details: dict[str, Any] = field(default_factory=dict)
    component: str | None = None
    thread_id: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z"
    )

    def to_interrupt(self) -> dict[str, Any]:
        """Return a LangGraph-friendly interrupt payload (pure mapping)."""
        with start_span("graph.interrupt.serialize"):
            return {
                "type": "human_interrupt",
                "name": self.name,
                "title": self.title,
                "message": self.message,
                "severity": self.severity,
                "details": _jsonify(self.details),
                "component": self.component,
                "thread_id": self.thread_id,
                "created_at": self.created_at,
            }


@dataclass(slots=True)
class HumanResponse:
    """Human response to an approval gate."""

    approved: bool
    comment: str | None = None
    updated: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "approved": bool(self.approved),
            "comment": self.comment,
            "updated": _jsonify(self.updated),
        }


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------

GATE_SQL_EXECUTION: Final[str] = "sql_execution"
GATE_EXTERNAL_CALL: Final[str] = "external_call"


def make_interrupt(
    *,
    name: str,
    title: str,
    message: str,
    severity: Literal["low", "medium", "high"] = "medium",
    details: Mapping[str, Any] | None = None,
    component: str | None = None,
    thread_id: str | None = None,
) -> dict[str, Any]:
    """Create a generic human interrupt payload."""
    gate = HumanGate(
        name=name,
        title=title,
        message=message,
        severity=severity,
        details=dict(details or {}),
        component=component,
        thread_id=thread_id,
    )
    return gate.to_interrupt()


def make_sql_gate(
    *,
    sql: str,
    params: Mapping[str, Any] | None = None,
    limit: int | None = None,
    tables: Sequence[str] | None = None,
    reason: str = "Confirm SQL execution",
) -> dict[str, Any]:
    """Build a standardized SQL approval gate.

    Notes
    -----
    - Only SELECT statements should be submitted. Callers must enforce read-only
      policies elsewhere; this gate exists for human awareness/approval.
    - Include a LIMIT when returning rows; Studio can highlight this.
    """
    details: dict[str, Any] = {
        "sql": str(sql).strip(),
        "params": _jsonify(dict(params or {})),
    }
    if limit is not None:
        details["limit"] = int(limit)
    if tables:
        details["tables"] = list(dict.fromkeys(str(t) for t in tables))

    gate = HumanGate(
        name=GATE_SQL_EXECUTION,
        title="Approve SQL execution",
        message=reason,
        severity="medium",
        details=details,
        component="agent.analytics.executor",
    )
    return gate.to_interrupt()


def make_external_call_gate(
    *,
    vendor: str,
    endpoint: str,
    payload: Mapping[str, Any] | None = None,
    method: str = "POST",
    reason: str = "Confirm external call",
) -> dict[str, Any]:
    """Build a standardized external-call approval gate."""
    details: dict[str, Any] = {
        "vendor": vendor,
        "endpoint": endpoint,
        "method": method.upper(),
        "payload": _jsonify(dict(payload or {})),
    }
    gate = HumanGate(
        name=GATE_EXTERNAL_CALL,
        title="Approve external call",
        message=reason,
        severity="high" if method.upper() in {"POST", "PUT", "DELETE"} else "medium",
        details=details,
        component="agent.common.integration",
    )
    return gate.to_interrupt()


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def parse_human_response(resp: Mapping[str, Any] | None) -> HumanResponse:
    """Parse a human response mapping into :class:`HumanResponse`.

    Accepts flexible keys: `approved`/`approve`/`ok` for the boolean decision,
    optional `comment`, and an optional `updated` payload.
    """
    r = dict(resp or {})
    decision = r.get("approved")
    if decision is None:
        decision = r.get("approve", r.get("ok"))
    approved = bool(decision)
    comment = r.get("comment")

    updated_raw = r.get("updated")
    updated = _jsonify(dict(updated_raw)) if isinstance(updated_raw, Mapping) else {}

    return HumanResponse(
        approved=approved, comment=str(comment) if comment is not None else None, updated=updated
    )


# ---------------------------------------------------------------------------
# JSON safety helpers
# ---------------------------------------------------------------------------


def _jsonify(v: Mapping[str, Any] | dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, val in dict(v).items():
        out[str(k)] = _coerce_primitive(val)
    return out


def _coerce_primitive(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, (bool, int, float, str)):  # noqa: UP038
        return v
    if isinstance(v, Sequence) and not isinstance(v, (str, bytes, bytearray)):  # noqa: UP038
        return [_coerce_primitive(x) for x in list(v)[:100]]
    if isinstance(v, Mapping):
        return _jsonify(dict(v))
    # Fallback: string repr
    try:
        return str(v)
    except Exception:  # pragma: no cover - very defensive
        return "<unserializable>"
