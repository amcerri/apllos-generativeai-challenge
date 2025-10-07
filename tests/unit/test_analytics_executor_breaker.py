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

import pytest

from app.agents.analytics.executor import AnalyticsExecutor


def test_dry_run_does_not_raise_on_missing_table(monkeypatch) -> None:
    exe = AnalyticsExecutor()
    # Non-existent table; dry_run should avoid actual execution
    plan = {"sql": "SELECT * FROM analytics.__does_not_exist__ LIMIT 1", "params": {}, "limit_applied": True}
    try:
        res = exe.execute(plan, dry_run=True, include_explain=True)
        assert isinstance(res.meta.get("explain"), (list, dict, type(None)))
    except Exception as exc:
        pytest.fail(f"dry_run raised unexpectedly: {exc}")


