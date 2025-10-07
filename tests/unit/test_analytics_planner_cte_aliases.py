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

"""Planner tests for CTEs and alias/schema prefix normalization.

These tests focus on SQL text properties returned by the planner, not on
execution. They validate that schema prefixes and alias normalization are
applied in common scenarios.
"""

from __future__ import annotations

import pytest


def test_planner_adds_schema_prefix_and_handles_cte_aliases():
    """Ensure planner schema-qualifies tables and fixes dotted aliases.

    Returns
    -------
    None
        Asserts SQL formatting properties only.
    """
    try:
        from app.agents.analytics.planner import AnalyticsPlanner
    except Exception:
        pytest.skip("planner unavailable")
        return

    allowlist = {
        "orders": [
            "order_id",
            "order_purchase_timestamp",
        ]
    }
    planner = AnalyticsPlanner()
    plan = planner.plan("count orders per month 2018", allowlist)
    sql = plan.sql.lower()
    # schema-qualified table
    assert "from analytics.orders" in sql
    # no dotted aliases like "AS analytics.orders"
    assert " as analytics." not in sql

