"""
Analytics SQL executor (read-only, bounded, timed).

Overview
--------
Executes planner-generated SQL with strict safety guarantees: read-only
transaction, server-side timeout, and client-side row cap. Converts DB rows to
plain dictionaries for downstream normalization.

Design
------
- **Read-only**: `SET LOCAL default_transaction_read_only = on` within a
  transaction. No DDL/DML allowed.
- **Timeout**: `SET LOCAL statement_timeout` (milliseconds).
- **Row cap**: stream rows and stop at `max_rows`, regardless of SQL LIMIT.
- **Explain (optional)**: `EXPLAIN (FORMAT JSON)`; can upgrade to ANALYZE only
  if explicitly enabled via env flag.
- **Zero hard deps**: the module imports `app.infra.db.get_engine()` lazily.
  If infra is absent at import time, it degrades gracefully.

Integration
-----------
- Consumes a plan compatible with `PlannerPlan` (fields: `sql`, `params`,
  `limit_applied`, `reason`).
- Returns an `ExecutorResult` with timing and diagnostics.
- Logging and tracing are optional but supported if infra is available.

Usage
-----
>>> from app.agents.analytics.executor import AnalyticsExecutor
>>> exe = AnalyticsExecutor()
>>> res = exe.execute({"sql": "SELECT 1 AS x", "params": {}}, max_rows=10)
>>> res.row_count, isinstance(res.rows, list)
(1, True)
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from time import monotonic
from typing import Any, Final

import sqlalchemy as sa

try:  # Optional logging
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:  # Optional config
    from app.config.settings import get_settings as get_config
except Exception:  # pragma: no cover - optional
    def get_config():
        return None


# Tracing (optional; use a single alias to avoid mypy signature clashes)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

__all__ = ["ExecutorResult", "AnalyticsExecutor"]


# ---------------------------------------------------------------------------
# Result contract
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class ExecutorResult:
    """Execution outcome for analytics queries.

    Attributes
    ----------
    rows: Materialized rows as dictionaries (capped by `row_cap`).
    row_count: Number of rows returned (≤ cap).
    exec_ms: Execution time in milliseconds (client-side measurement).
    limit_applied: Whether the planner injected a LIMIT (informational only).
    warnings: Non-fatal notes collected during execution.
    meta: Extra diagnostics (e.g., explain output, timings).
    """

    rows: list[dict[str, Any]]
    row_count: int
    exec_ms: float
    limit_applied: bool
    warnings: list[str]
    meta: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "rows": [dict(r) for r in self.rows],
            "row_count": int(self.row_count),
            "exec_ms": float(self.exec_ms),
            "limit_applied": bool(self.limit_applied),
            "warnings": list(self.warnings),
            "meta": dict(self.meta),
        }


# ---------------------------------------------------------------------------
# Executor
# ---------------------------------------------------------------------------
# Simple in-process circuit breaker (per-sql-hash)
_BREAKER_FAILURES: dict[str, int] = {}
_BREAKER_OPEN_UNTIL: dict[str, float] = {}
_BREAKER_MAX_FAILURES: Final[int] = 3
_BREAKER_RESET_AFTER_S: Final[float] = 60.0


def _sql_key(sql: str) -> str:
    import hashlib
    return hashlib.sha256(sql.strip().encode("utf-8")).hexdigest()[:16]


class AnalyticsExecutor:
    """Read-only SQL executor with server-side timeout and row cap."""

    def __init__(self) -> None:
        self.log = get_logger("agent.analytics.executor")
        self._config = get_config()
        
        # Get configuration values with fallbacks using Settings model
        try:
            executor_cfg = getattr(getattr(self._config, "analytics"), "executor")  # type: ignore[attr-defined]
            self.default_timeout_s = int(getattr(executor_cfg, "default_timeout_seconds", 60))
            self.default_row_cap = int(getattr(executor_cfg, "default_row_cap", 2000))
            self.max_row_cap = int(getattr(executor_cfg, "max_row_cap", 10000))
        except Exception:
            self.default_timeout_s = 60
            self.default_row_cap = 2000
            self.max_row_cap = 10000

    def execute(
        self,
        plan: Mapping[str, Any] | Any,
        *,
        max_rows: int | None = None,
        timeout_s: int | None = None,
        readonly: bool = True,
        include_explain: bool = False,
        dry_run: bool = False,
    ) -> ExecutorResult:
        """Execute the given plan and return an :class:`ExecutorResult`.

        Parameters
        ----------
        plan: A mapping or object with attributes `sql`, `params`,
            and optional `limit_applied`.
        max_rows: Client-side cap (defaults to :data:`DEFAULT_ROW_CAP`).
        timeout_s: Server-side `statement_timeout` in seconds
            (defaults to :data:`DEFAULT_TIMEOUT_S`).
        readonly: If True, enforce `default_transaction_read_only = on`.
        include_explain: If True, attach `EXPLAIN (FORMAT JSON)` in `meta`.
        dry_run: When True, perform EXPLAIN-only without returning data rows.
        """

        # Extract plan fields with a tolerant adapter
        sql = _get_attr(plan, "sql", default="").strip()
        if not sql:
            raise ValueError("empty SQL in plan")
        params = _get_attr(plan, "params", default={}) or {}
        limit_applied = bool(_get_attr(plan, "limit_applied", default=False))

        # Safety gate: must be a pure SELECT, without DDL/DML verbs
        _assert_safe_select(sql)

        # Circuit breaker: short-circuit when open
        key = _sql_key(sql)
        now = monotonic()
        open_until = _BREAKER_OPEN_UNTIL.get(key)
        if open_until and now < open_until:
            raise RuntimeError("circuit_open: skipping execution due to repeated failures")

        # Reinstate a configurable row cap to avoid unbounded memory usage.
        # Defaults come from settings; callers can override via `max_rows`.
        cap = int(max_rows or self.default_row_cap)
        cap = max(1, min(cap, self.max_row_cap))  # hard upper bound safeguard

        # Heuristic: for aggregation queries (GROUP BY), raise cap to max to
        # avoid truncating small categorical sets (e.g., 27 estados), while
        # still maintaining a hard safety upper bound.
        sql_lower = sql.lower()
        if " group by " in sql_lower and cap < self.max_row_cap:
            cap = self.max_row_cap
        timeout = int(timeout_s or self.default_timeout_s)

        # Get engine lazily (avoid hard import on module import)
        engine = _get_engine()

        rows: list[dict[str, Any]] = []
        warnings: list[str] = []
        explain_json: Any | None = None

        with start_span("agent.analytics.execute", {"row_cap": "unlimited", "timeout_s": timeout}):
            t0 = monotonic()
            try:
                with engine.begin() as conn:  # transactional context for SET LOCAL
                    if readonly:
                        conn.exec_driver_sql("SET LOCAL default_transaction_read_only = on")
                    # timeout in milliseconds
                    conn.exec_driver_sql(f"SET LOCAL statement_timeout = {timeout * 1000}")

                    if dry_run:
                        # EXPLAIN only; no data retrieval
                        explain_json = _explain_json(conn, sql, params)
                    else:
                        # Stream results
                        result = conn.execution_options(stream_results=True).execute(
                            sa.text(sql), params
                        )
                        for mapping in result.mappings():
                            rows.append(dict(mapping))
                            if len(rows) >= cap:
                                break

                        if include_explain:
                            explain_json = _explain_json(conn, sql, params)

                # reset breaker counter on success
                _BREAKER_FAILURES.pop(key, None)
                _BREAKER_OPEN_UNTIL.pop(key, None)

            except Exception as exc:  # capture and continue with diagnostics
                warnings.append(f"execution_error: {type(exc).__name__}")
                # increment breaker failures and open if threshold crossed
                fail = _BREAKER_FAILURES.get(key, 0) + 1
                _BREAKER_FAILURES[key] = fail
                if fail >= _BREAKER_MAX_FAILURES:
                    _BREAKER_OPEN_UNTIL[key] = now + _BREAKER_RESET_AFTER_S
                raise
            finally:
                exec_ms = (monotonic() - t0) * 1000.0

        # Sanitize SQL in meta based on environment flag (default: show full SQL).
        sanitize = os.getenv("EXECUTOR_SANITIZE_SQL", "false").strip().lower() in {"1", "true", "yes"}
        sql_preview = _preview_sql(sql) if sanitize else sql

        meta: dict[str, Any] = {
            "sql": sql_preview,
            "row_cap": cap,
            "timeout_s": timeout,
            "explain": explain_json,
            "circuit_failures": _BREAKER_FAILURES.get(key, 0),
            "circuit_open_until": _BREAKER_OPEN_UNTIL.get(key),
        }

        return ExecutorResult(
            rows=rows,
            row_count=len(rows),
            exec_ms=exec_ms,
            limit_applied=limit_applied,
            warnings=warnings,
            meta=meta,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_attr(obj: Mapping[str, Any] | Any, name: str, *, default: Any) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _assert_safe_select(sql: str) -> None:
    sql_l = sql.lstrip().lower()
    # Disallow multiple statements via semicolons (stacked statements)
    if ";" in sql_l:
        raise ValueError("multiple statements are not allowed")
    # Allow SELECT and WITH (CTEs) statements
    if not (sql_l.startswith("select") or sql_l.startswith("with")):
        raise ValueError("only SELECT and WITH statements are allowed")

    blocked = {"insert", "update", "delete", "alter", "drop", "create", "grant", "revoke"}
    tokens = {t for t in sql_l.replace("\n", " ").split(" ") if t}
    if any(b in tokens for b in blocked):
        raise ValueError("DDL/DML tokens are not allowed in executor SQL")

    # Optional function allowlist (best-effort): reject unknown function calls
    _ALLOWED_FUNCS = {
        "count", "sum", "avg", "min", "max", "coalesce", "nullif", "date_trunc", "extract",
        "upper", "lower", "substring", "round", "floor", "ceil", "greatest", "least",
    }
    import re as _re
    for m in _re.finditer(r"\b([a-z_][a-z0-9_]*)\s*\(", sql_l):
        fname = m.group(1)
        if fname not in _ALLOWED_FUNCS and fname not in {"select", "with"}:
            raise ValueError(f"function not allowed: {fname}")

    # Block access to pg_catalog or information_schema explicitly
    if "pg_catalog" in sql_l or "information_schema" in sql_l:
        raise ValueError("system catalogs are not allowed")


def _get_engine():
    try:
        from app.infra.db import get_engine  # local import to keep it optional
    except Exception as exc:  # pragma: no cover - optional
        raise RuntimeError("database engine accessor not available") from exc
    return get_engine()


def _explain_json(conn: Any, sql: str, params: Mapping[str, Any]) -> Any | None:
    """Return EXPLAIN output as JSON (no ANALYZE by default).

    Uses `EXPLAIN (FORMAT JSON)`. To enable ANALYZE, set env var
    `APP_EXPLAIN_ANALYZE=true` (runs the query inside EXPLAIN).
    """

    analyze = os.getenv("APP_EXPLAIN_ANALYZE", "false").strip().lower() in {"1", "true", "yes"}
    clause = "EXPLAIN (FORMAT JSON) " if not analyze else "EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) "
    try:
        res = conn.execute(sa.text(clause + sql), params)
        row = res.first()
        if row is None:
            return None
        # In Postgres, FORMAT JSON returns a single column containing a JSON value
        first_val = row[0]
        return first_val
    except Exception as exc:  # best-effort; attach warning only
        # Do not raise—record diagnostics in meta via caller
        return {"error": type(exc).__name__, "message": str(exc)}


def _preview_sql(sql: str, *, max_len: int = 220) -> str:
    """Return a safe preview of the SQL for meta/logs.

    Parameters
    ----------
    sql : str
        Full SQL text.
    max_len : int
        Maximum length of the preview string.

    Returns
    -------
    str
        Preview string with whitespace collapsed and truncated.
    """
    s = (sql or "").strip()
    s = " ".join(s.split())
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s
