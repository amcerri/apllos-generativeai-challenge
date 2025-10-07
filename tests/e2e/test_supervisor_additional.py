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

"""Additional supervisor routing tests.

Covers single-pass fallback when document-style signals are present and
analytics signals are weak.
"""

from __future__ import annotations

import pytest


def test_supervisor_fallback_to_knowledge_when_doc_cues():
    """Assert supervisor falls back analytics→knowledge on doc cues.

    Returns
    -------
    None
        Asserts the expected agent decision.
    """
    try:
        from app.routing.supervisor import supervise, RoutingContext
    except Exception:
        pytest.skip("routing supervisor unavailable")
        return

    dec = {
        "agent": "analytics",
        "confidence": 0.55,
        "reason": "weak allowlist",
        "tables": [],
        "columns": [],
        "signals": ["doc_style"],
        "thread_id": None,
    }
    out = supervise(dec, RoutingContext())
    assert isinstance(out, dict)
    assert out.get("agent") == "knowledge"

