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
from app.agents.analytics.planner import _validate_identifiers


def test_executor_blocks_semicolons() -> None:
    with pytest.raises(ValueError):
        _assert_safe_select("SELECT 1; SELECT 2")


def test_executor_blocks_unknown_functions() -> None:
    with pytest.raises(ValueError):
        _assert_safe_select("SELECT unsafe_func(order_id) FROM analytics.orders")


def test_planner_blocks_system_catalogs() -> None:
    with pytest.raises(ValueError):
        _validate_identifiers("SELECT * FROM pg_catalog.pg_tables", {"orders": ["order_id"]})


