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

"""Test scaffolding for dry-run (EXPLAIN) behavior when approval rejected.

This unit-level test emulates plan execution path and asserts that the meta
contains an `explain` key, indicating EXPLAIN was attempted. Full graph
execution is covered separately in E2E.
"""

from __future__ import annotations

import pytest


def test_executor_explain_present_in_meta_on_dry_run(monkeypatch):
    """Assert that meta includes `explain` in dry-run scenarios.

    Returns
    -------
    None
        Validates presence of `explain` without executing real queries.
    """
    try:
        from app.agents.analytics.executor import AnalyticsExecutor
    except Exception:
        pytest.skip("executor unavailable")
        return

    exe = AnalyticsExecutor()
    plan = {"sql": "SELECT 1", "params": {}, "limit_applied": False}
    res = exe.execute(plan, max_rows=1, timeout_s=1, dry_run=True, include_explain=True)
    # `explain` can be None or a structure; assert key exists
    assert "explain" in res.meta

