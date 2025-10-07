"""
Analytics agent package initializer

Overview
    Side‑effect‑free initializer for the **analytics** agent. This package will
    contain three stages executed in order: **planner** → **executor** → **normalize**.
    The agent answers tabular questions over Olist data through **safe SQL** using
    an allowlist; the final user response is business‑friendly in pt‑BR.

Design
    - Keep this module lightweight (no I/O, no dynamic imports).
    - Do **not** import submodules here to avoid early side effects/cycles.
    - Provide discovery helpers that return **paths** to stage modules.

Integration
    - Other parts of the app can inspect available stages via `stages()` and
      resolve `stage_path(name)` without importing the stage implementations yet.

Usage
    >>> from app.agents.analytics import stages, has_stage, stage_path
    >>> stages()
    ('planner', 'executor', 'normalize')
    >>> has_stage('planner')
    True
    >>> stage_path('normalize').name
    'normalize.py'
"""

from __future__ import annotations

from app.agents.analytics.planner import AnalyticsPlanner


def test_planner_timeseries_heuristic_infers_date_trunc() -> None:
    allowlist = {
        "orders": [
            "order_id",
            "order_purchase_timestamp",
            "order_status",
        ]
    }
    p = AnalyticsPlanner()
    plan = p.plan("Pedidos por mês em 2018", allowlist)
    sql = plan.sql.lower()
    assert "date_trunc('month'" in sql or "date_trunc('month'" in sql


def test_planner_preview_has_limit() -> None:
    allowlist = {"orders": ["order_id", "order_purchase_timestamp", "order_status"]}
    p = AnalyticsPlanner()
    plan = p.plan("Listar pedidos", allowlist)
    assert plan.limit_applied is True
    assert " limit " in plan.sql.lower()


