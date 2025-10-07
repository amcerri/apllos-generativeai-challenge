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

from app.agents.analytics.planner import _validate_joins


def test_validate_joins_blocks_cross_schema() -> None:
    allowlist = {"orders": ["order_id"]}
    sql = "SELECT 1 FROM analytics.orders JOIN other.schema ON 1=1"
    with pytest.raises(ValueError):
        _validate_joins(sql, allowlist)


def test_validate_joins_blocks_non_allowlisted_table() -> None:
    allowlist = {"orders": ["order_id"]}
    sql = "SELECT 1 FROM analytics.orders JOIN analytics.unknown ON 1=1"
    with pytest.raises(ValueError):
        _validate_joins(sql, allowlist)


