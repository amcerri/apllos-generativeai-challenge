"""
RouterDecision Contract

Overview
    Strict dataclass and helpers for the router → supervisor interface. The
    classifier must emit a `RouterDecision` instance serialized as JSON (or a
    Python dict) that adheres to this contract exactly.

Design
    - Strong typing via `Literal` for `agent` and simple runtime validation.
    - No external dependencies; stdlib only.
    - JSON Schema provided for LLM Structured Outputs and validation tools.

Integration
    - Use `RouterDecision.from_dict(...)` to validate/construct from LLM output.
    - Use `RouterDecision.JSON_SCHEMA` when configuring Structured Outputs.
    - The supervisor should trust only validated instances.

Usage
    >>> payload = {
    ...   "agent": "analytics", "confidence": 0.77, "reason": "mentions tables",
    ...   "tables": ["orders"], "columns": ["order_id"], "signals": ["allowlist-hit"],
    ... }
    >>> rd = RouterDecision.from_dict(payload)
    >>> rd.agent, rd.confidence
    ('analytics', 0.77)
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any, Final, Literal, cast

# ---------------------------------------------------------------------------
# Canonical agent names and schema
# ---------------------------------------------------------------------------
AgentName = Literal["analytics", "knowledge", "commerce", "triage"]
_AGENT_VALUES: Final[tuple[str, ...]] = ("analytics", "knowledge", "commerce", "triage")
_ALLOWED_KEYS: Final[tuple[str, ...]] = (
    "agent",
    "confidence",
    "reason",
    "tables",
    "columns",
    "signals",
    "thread_id",
)

__all__: Final[list[str]] = ["AgentName", "RouterDecision", "ROUTER_DECISION_JSON_SCHEMA"]

# JSON Schema for Structured Outputs
ROUTER_DECISION_JSON_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "RouterDecision",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "agent": {
            "type": "string",
            "enum": list(_AGENT_VALUES),
            "description": "Target agent name",
        },
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Classifier confidence in [0,1]",
        },
        "reason": {
            "type": "string",
            "minLength": 1,
            "description": "Short justification for the route",
        },
        "tables": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Referenced/recognized tables",
            "default": [],
        },
        "columns": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Referenced/recognized columns",
            "default": [],
        },
        "signals": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Routing signals (allowlist-hit, rag-hit, etc.)",
            "default": [],
        },
    },
    "required": ["agent", "confidence", "reason"],
}


def _norm_list_str(values: Iterable[Any] | None) -> list[str]:
    """Best-effort normalize to a list[str] with unique, non-empty items.

    - Accepts lists/tuples/sets/iterables; `None` → empty list.
    - Casts each item to `str`, strips whitespace, removes empties and duplicates
      while preserving first-seen order.
    """

    if not values:
        return []
    seen = set()
    out: list[str] = []
    for v in values:
        s = str(v).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _is_valid_agent(value: str) -> bool:
    return value in _AGENT_VALUES


@dataclass(slots=True)
class RouterDecision:
    """Router output contract with minimal runtime validation.

    Fields
        agent: one of {analytics, knowledge, commerce, triage}
        confidence: float in [0.0, 1.0]
        reason: short string explaining the choice
        tables: list of table names the classifier detected
        columns: list of column names the classifier detected
        signals: list of routing signals (e.g., allowlist-hit, rag-hit)
        thread_id: optional thread identifier for cross-run correlation
    """

    agent: AgentName
    confidence: float
    reason: str
    tables: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    thread_id: str | None = None

    # ---------------------------
    # Validation & normalization
    # ---------------------------
    def __post_init__(self) -> None:
        # agent
        if not _is_valid_agent(self.agent):
            raise ValueError(f"invalid agent '{self.agent}'; must be one of {_AGENT_VALUES}")

        # confidence
        try:
            c = float(self.confidence)
        except (TypeError, ValueError) as exc:  # pragma: no cover - guard
            raise ValueError("confidence must be a float in [0, 1]") from exc
        if not (0.0 <= c <= 1.0):
            raise ValueError("confidence must be between 0.0 and 1.0 (inclusive)")
        self.confidence = c

        # reason
        r = (self.reason or "").strip()
        if not r:
            raise ValueError("reason must be a non-empty string")
        # keep it short but don't truncate; downstream can log/display fully
        self.reason = r

        # lists normalization
        self.tables = _norm_list_str(self.tables)
        self.columns = _norm_list_str(self.columns)
        self.signals = _norm_list_str(self.signals)

        # thread_id normalization
        if self.thread_id is not None:
            tid = str(self.thread_id).strip()
            self.thread_id = tid or None

    # ---------------------------
    # Conversions
    # ---------------------------
    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict (JSON-serializable)."""

        return {
            "agent": self.agent,
            "confidence": self.confidence,
            "reason": self.reason,
            "tables": list(self.tables),
            "columns": list(self.columns),
            "signals": list(self.signals),
            "thread_id": self.thread_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RouterDecision:
        """Construct a validated instance from a mapping.

        Raises
            ValueError: when required fields are missing/invalid or when unknown
            keys are provided (strict parsing).
        """

        if not isinstance(data, Mapping):  # pragma: no cover - defensive
            raise ValueError("data must be a mapping")

        # Unknown key check (strict)
        unknown = set(data.keys()) - set(_ALLOWED_KEYS)
        if unknown:
            raise ValueError(f"unknown keys in RouterDecision: {sorted(unknown)}")

        try:
            agent_raw = data["agent"]
            confidence_raw = data["confidence"]
            reason_raw = data["reason"]
        except KeyError as exc:
            raise ValueError(f"missing required field: {exc.args[0]}") from exc

        tables = data.get("tables")
        columns = data.get("columns")
        signals = data.get("signals")
        thread_id = data.get("thread_id")

        agent_str = str(agent_raw)
        # Let float() raise if not convertible; __post_init__ enforces bounds
        confidence_val = float(confidence_raw)
        reason_str = str(reason_raw)

        return cls(
            agent=cast(AgentName, agent_str),
            confidence=confidence_val,
            reason=reason_str,
            tables=_norm_list_str(tables if isinstance(tables, Iterable) else None),
            columns=_norm_list_str(columns if isinstance(columns, Iterable) else None),
            signals=_norm_list_str(signals if isinstance(signals, Iterable) else None),
            thread_id=(str(thread_id).strip() or None) if thread_id is not None else None,
        )


    @classmethod
    def schema(cls) -> dict[str, Any]:
        """Return a (shallow) copy of the JSON Schema dict."""

        return dict(ROUTER_DECISION_JSON_SCHEMA)
