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

from app.agents.analytics.executor import _assert_safe_select


def test_executor_rejects_non_select() -> None:
    with pytest.raises(ValueError):
        _assert_safe_select("DELETE FROM analytics.orders")


def test_executor_allows_select_and_with() -> None:
    _assert_safe_select("SELECT 1")
    _assert_safe_select("WITH cte AS (SELECT 1) SELECT * FROM cte")


