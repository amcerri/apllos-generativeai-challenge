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

"""Tests for allowlist loading behavior.

Ensures assistant loads allowlist from JSON when present and falls back to an
embedded mapping otherwise.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest


def test_allowlist_loads_from_json(tmp_path: Path, monkeypatch):
    """Load allowlist from JSON file and assert content.

    Parameters
    ----------
    tmp_path : Path
        Temporary path fixture provided by pytest.
    monkeypatch : MonkeyPatch
        Fixture for environment isolation (not used directly here).

    Returns
    -------
    None
        Asserts the expected behavior.
    """
    try:
        from app.graph.assistant import _load_allowlist
    except Exception:
        pytest.skip("assistant unavailable")
        return

    # Prepare a temporary allowlist file
    allowlist_dir = Path(__file__).parents[2] / "app" / "routing"
    allowlist_file = allowlist_dir / "allowlist.json"
    allowlist_dir.mkdir(parents=True, exist_ok=True)
    content = {"orders": ["order_id", "order_status"]}
    allowlist_file.write_text(json.dumps(content), encoding="utf-8")

    try:
        al = _load_allowlist()
        assert isinstance(al, dict)
        assert "orders" in al and "order_id" in al["orders"]
    finally:
        try:
            allowlist_file.unlink()
        except Exception:
            pass

