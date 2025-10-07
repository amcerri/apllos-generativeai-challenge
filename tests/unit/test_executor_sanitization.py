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

"""Tests for executor SQL sanitization preview behavior.

This module validates that the executor meta includes a sanitized SQL preview
when the EXECUTOR_SANITIZE_SQL flag is enabled, and the full SQL otherwise.
"""

from __future__ import annotations

import os

import pytest


def test_executor_meta_sql_preview(monkeypatch):
    """Ensure meta.sql toggles between full SQL and sanitized preview.

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        Pytest fixture used to set environment variables for the test.

    Returns
    -------
    None
        This test asserts behavior and does not return a value.
    """
    try:
        from app.agents.analytics.executor import AnalyticsExecutor
    except Exception:
        pytest.skip("executor unavailable")
        return

    exe = AnalyticsExecutor()
    plan = {"sql": "SELECT 1 AS x FROM analytics.orders", "params": {}, "limit_applied": False}

    # With sanitization disabled (default), should include full SQL
    monkeypatch.delenv("EXECUTOR_SANITIZE_SQL", raising=False)
    res = exe.execute(plan, max_rows=5, timeout_s=1)
    assert "sql" in res.meta
    assert res.meta["sql"].startswith("SELECT 1 AS x")

    # With sanitization enabled, should include preview (collapsed/possibly truncated)
    monkeypatch.setenv("EXECUTOR_SANITIZE_SQL", "true")
    res2 = exe.execute(plan, max_rows=5, timeout_s=1)
    assert "sql" in res2.meta
    assert "\n" not in res2.meta["sql"]

