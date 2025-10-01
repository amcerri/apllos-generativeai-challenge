"""
Analytics planner (safe SQL synthesis).

Overview
--------
Translate natural‑language analytical requests into **safe, bounded SQL** over the
Olist analytics schema. The planner enforces hard guardrails: no `SELECT *`,
no DDL/DML, only allow‑listed identifiers, and a **LIMIT** for non‑aggregate
queries. It returns a structured plan object for downstream execution and
normalization.

Design
------
- Stateless planner with a deterministic fallback (no network), plus optional LLM
  backend (wired later) via prompts in `app/prompts/analytics/`.
- Guardrails first: identifiers are validated against an explicit allowlist
  (table → columns). Aggregations prefer `COUNT(1)` instead of `COUNT(*)`.
- Heuristics cover common intents: preview with cap, counts, top‑N, and time
  series using `date_trunc` when a timestamp column is available.

Integration
-----------
- Called by the analytics agent node before execution.
- Logging uses structlog (component/event/thread_id). Tracing spans are optional.
- The resulting plan is handed to the executor; SQL strings are not shown to
  end users (only business narratives are surfaced by the normalizer).

Usage
-----
>>> from app.agents.analytics.planner import AnalyticsPlanner
>>> allowlist = {"orders": ["order_id", "order_status", "order_purchase_timestamp", "customer_id"],
...              "order_items": ["order_id", "price", "freight_value", "product_id", "seller_id"]}
>>> planner = AnalyticsPlanner()
>>> plan = planner.plan("Orders per month in 2018", allowlist, thread_id="t-123")
>>> plan.sql.startswith("SELECT") and plan.limit_applied in (True, False)
True
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Final

start_span: Any

try:  # Logging & tracing are optional at import time
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


try:  # Optional tracing
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

__all__ = ["PlannerPlan", "AnalyticsPlanner"]


# ---------------------------------------------------------------------------
# Data contract
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class PlannerPlan:
    """Represent a safe SQL plan for execution.

    Attributes
    ----------
    sql: Final SQL string to be executed by the executor (read‑only intent).
    params: Query parameters (future use; keep for compatibility).
    reason: Short English rationale for traceability.
    limit_applied: Whether a LIMIT was injected due to non‑aggregate query.
    warnings: Non‑fatal observations (e.g., heuristic assumptions).
    """

    sql: str
    params: dict[str, Any]
    reason: str
    limit_applied: bool
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict representation."""

        return {
            "sql": self.sql,
            "params": dict(self.params),
            "reason": self.reason,
            "limit_applied": bool(self.limit_applied),
            "warnings": list(self.warnings),
        }


# ---------------------------------------------------------------------------
# Planner
# ---------------------------------------------------------------------------
class AnalyticsPlanner:
    """Synthesize safe SQL bounded by an allowlist and simple heuristics.

    This deterministic implementation avoids network calls and is sufficient for
    unit/e2e tests. An optional LLM backend can be introduced later using the
    prompts authored under `app/prompts/analytics/`.
    """

    DEFAULT_PREVIEW_LIMIT: Final[int] = 200
    MAX_SAFE_LIMIT: Final[int] = 5000

    def __init__(self) -> None:
        self.log = get_logger("agent.analytics.planner")

    # Public API -------------------------------------------------------------
    def plan(
        self,
        query: str,
        allowlist: Mapping[str, Iterable[str]],
        *,
        thread_id: str | None = None,
        default_limit: int | None = None,
    ) -> PlannerPlan:
        """Produce a safe SQL plan.

        Args:
            query: Natural‑language request.
            allowlist: Mapping of table → columns allowed for selection.
            thread_id: Correlation id for logging/tracing.
            default_limit: Optional per‑call LIMIT for non‑aggregate previews.

        Returns:
            PlannerPlan: Structured plan with SQL and guardrail metadata.
        """

        cap = int(default_limit or self.DEFAULT_PREVIEW_LIMIT)
        cap = max(1, min(cap, self.MAX_SAFE_LIMIT))

        with start_span("agent.analytics.plan", {"thread_id": thread_id}):
            logger = self.log.bind(component="agent.analytics", event="plan", thread_id=thread_id)

            text = (query or "").strip()
            lw = text.lower()
            tables_index = _normalize_allowlist(allowlist)

            table = _pick_table(text, tables_index) or _fallback_table(tables_index)
            if not table:
                sql = "SELECT 1 WHERE 1=0"  # unreachable sentinel; no schema
                return PlannerPlan(
                    sql=sql,
                    params={},
                    reason="no available tables in allowlist",
                    limit_applied=True,
                    warnings=["empty_allowlist"],
                )
            
            # Get columns from allowlist
            cols = tables_index[table]
            
            # Add schema prefix for SQL generation
            if not table.startswith("analytics."):
                table = f"analytics.{table}"
            is_agg = _is_aggregation_intent(lw)
            timescale = _detect_timescale(lw)
            ts_col = _find_time_column(cols)

            year = _extract_year(lw)

            warnings: list[str] = []

            if is_agg and timescale and ts_col:
                # Timeseries aggregation
                where = ""
                if year and ts_col:
                    where = (
                        f"WHERE {table}.{ts_col} >= '{year}-01-01' AND "
                        f"{table}.{ts_col} < '{year + 1}-01-01'"
                    )
                sql = (
                    f"SELECT date_trunc('{timescale}', {table}.{ts_col}) AS period, COUNT(1) AS qty\n"
                    f"FROM {table}\n"
                    f"{where}\n"
                    f"GROUP BY period\n"
                    f"ORDER BY period"
                ).replace("\n\n", "\n")
                limit_applied = False
                reason = f"{timescale} time series using {ts_col}"
            elif is_agg:
                # Global aggregation (count)
                if year and ts_col:
                    sql = (
                        f"SELECT COUNT(1) AS qty\n"
                        f"FROM {table}\n"
                        f"WHERE {table}.{ts_col} >= '{year}-01-01' AND "
                        f"{table}.{ts_col} < '{year + 1}-01-01'"
                    )
                else:
                    sql = f"SELECT COUNT(1) AS qty FROM {table}"
                limit_applied = False
                reason = "global count"
            else:
                # Preview with cap: choose a small set of explicit columns
                preview_cols = _choose_preview_columns(cols)
                where = ""
                if year and ts_col:
                    where = (
                        f"WHERE {table}.{ts_col} >= '{year}-01-01' AND "
                        f"{table}.{ts_col} < '{year + 1}-01-01'"
                    )
                sql = (
                    f"SELECT {', '.join(f'{table}.{c}' for c in preview_cols)}\n"
                    f"FROM {table}\n"
                    f"{where}\n"
                    f"ORDER BY 1 DESC\n"
                    f"LIMIT {cap}"
                ).replace("\n\n", "\n")
                limit_applied = True
                reason = "capped preview"

            # Final safety checks (syntactic only; executor enforces read‑only)
            if "*" in sql:
                warnings.append("select_star_blocked")
                sql = sql.replace("*", "1")  # ultra‑conservative fallback

            # Create validation allowlist with schema prefix to match the SQL
            validation_allowlist = {table: cols}
            _validate_identifiers(sql, validation_allowlist)  # raises on violation

            logger.info("Planned SQL", sql=sql, reason=reason)
            return PlannerPlan(
                sql=sql, params={}, reason=reason, limit_applied=limit_applied, warnings=warnings
            )


# ---------------------------------------------------------------------------
# Heuristics & helpers
# ---------------------------------------------------------------------------

_AGG_KEYS = (
    "count",
    "quantos",
    "qtd",
    "quantidade",
    "número de",
    "numero de",
    "total",
    "soma",
    "sum",
    "média",
    "media",
    "avg",
    "taxa",
    "percentual",
    "distribuição",
    "distribuicao",
)

_MONTH_KEYS = ("por mês", "mensal", "month", "monthly")
_WEEK_KEYS = ("por semana", "semanal", "week", "weekly")
_DAY_KEYS = ("por dia", "diário", "diario", "day", "daily")
_YEAR_KEYS = ("por ano", "anual", "year", "yearly")

_TIME_HINTS = ("timestamp", "date", "data", "dt")

_IDENTIFIER_RE = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")


def _normalize_allowlist(allowlist: Mapping[str, Iterable[str]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for t, cols in allowlist.items():
        t2 = str(t).strip()
        if not t2:
            continue
        cset = sorted({str(c).strip() for c in cols if str(c).strip()})
        out[t2] = cset
    return dict(sorted(out.items(), key=lambda kv: kv[0]))


def _pick_table(text: str, tables_index: Mapping[str, list[str]]) -> str | None:
    tokens = {w.strip(".,:;()[]{}\"'`").lower() for w in text.split()}
    for t in tables_index.keys():
        if t.lower() in tokens:
            return t
    # Common default preference
    for preferred in ("orders", "order_items", "customers", "products"):
        if preferred in tables_index:
            return preferred
    return None


def _fallback_table(tables_index: Mapping[str, list[str]]) -> str | None:
    return next(iter(tables_index.keys()), None)


def _is_aggregation_intent(lw: str) -> bool:
    return any(k in lw for k in _AGG_KEYS)


def _detect_timescale(lw: str) -> str | None:
    if any(k in lw for k in _MONTH_KEYS):
        return "month"
    if any(k in lw for k in _WEEK_KEYS):
        return "week"
    if any(k in lw for k in _DAY_KEYS):
        return "day"
    if any(k in lw for k in _YEAR_KEYS):
        return "year"
    return None


_YEAR_RE = re.compile(r"(?<!\d)(19|20)\d{2}(?!\d)")


def _extract_year(lw: str) -> int | None:
    """Return a 4-digit year if present (e.g., 2018), else None."""
    m = _YEAR_RE.search(lw)
    if not m:
        return None
    try:
        return int(m.group(0))
    except Exception:
        return None


def _find_time_column(columns: list[str]) -> str | None:
    lwcols = [c.lower() for c in columns]
    for hint in _TIME_HINTS:
        for c in lwcols:
            if hint in c:
                # return original‑case column
                return columns[lwcols.index(c)]
    return None


def _choose_preview_columns(columns: list[str], *, max_cols: int = 6) -> list[str]:
    # Prefer id/status/timestamps first, then fill in with the next columns.
    priority = [
        *[c for c in columns if c.endswith("_id")],
        *[c for c in columns if "status" in c],
        *[c for c in columns if any(h in c for h in ("timestamp", "date", "dt"))],
    ]
    rest = [c for c in columns if c not in priority]
    ordered = []
    for c in priority + rest:
        if c not in ordered:
            ordered.append(c)
        if len(ordered) >= max_cols:
            break
    return ordered or columns[: min(max_cols, len(columns))]


def _validate_identifiers(sql: str, allowlist: Mapping[str, Iterable[str]]) -> None:
    # Extract bare tokens and ensure all table.column references are allowed.
    tokens = set(_IDENTIFIER_RE.findall(sql))
    # Quick reject for DDL/DML verbs
    blocked = {"insert", "update", "delete", "alter", "drop", "create", "grant", "revoke"}
    if any(b in (t.lower()) for t in tokens for b in blocked):
        raise ValueError("DDL/DML tokens are not allowed in planner SQL")

    # Allow functions and keywords implicitly; enforce on identifiers
    tables = set(allowlist)
    columns = set()
    for cols in allowlist.values():
        columns.update({str(c) for c in cols})

    # Validate column names that appear after a dot (table.column)
    # Only match patterns that have at least one dot before the column name
    for m in re.finditer(r"([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+)\.([a-zA-Z_][a-zA-Z0-9_]*)", sql):
        t, c = m.group(1), m.group(2)
        # Check both with and without schema prefix
        table_without_schema = t.replace("analytics.", "") if t.startswith("analytics.") else t
        # Check if table exists in allowlist (with or without schema prefix)
        table_found = t in tables or table_without_schema in tables
        if not table_found or c not in columns:
            raise ValueError(f"identifier not allowed: {t}.{c}")

    # Validate FROM clause tables
    for m in re.finditer(r"\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\b", sql, flags=re.IGNORECASE):
        t = m.group(1)
        # Check both with and without schema prefix
        table_without_schema = t.replace("analytics.", "") if t.startswith("analytics.") else t
        table_found = t in tables or table_without_schema in tables
        if not table_found:
            raise ValueError(f"table not allowed: {t}")
