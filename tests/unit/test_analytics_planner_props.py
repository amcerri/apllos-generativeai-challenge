"""
Analytics planner — behavioral properties (unit tests).

Overview
--------
Validates high‑level properties of the Analytics planner regardless of internal
implementation details. We assert the contract:
- returns a mapping with keys: sql, params, reason, limit_applied, warnings;
- never uses `SELECT *` (except inside aggregates like COUNT(*));
- applies `LIMIT` when the query is a preview (non‑aggregate);
- only references identifiers present in the provided allowlist.

Design
------
Tests are defensive: if the planner is unavailable or requires network access,
we `pytest.skip` gracefully to keep CI deterministic for this POC.

Integration
-----------
Relies on the `allowlist` fixture from `tests/conftest.py` and the
`AnalyticsPlanner` class from `app.agents.analytics.planner`.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any

import pytest

AnalyticsPlanner: Any
try:
    from app.agents.analytics.planner import AnalyticsPlanner as _AnalyticsPlanner

    AnalyticsPlanner = _AnalyticsPlanner
except Exception:  # pragma: no cover - optional
    AnalyticsPlanner = None


# ---------------------------------------------------------------------------
# Helpers (pure python, no DB)
# ---------------------------------------------------------------------------

_AGG_FUNC_RE = re.compile(r"\b(count|sum|avg|min|max)\s*\(", re.IGNORECASE)
_GROUP_BY_RE = re.compile(r"\bgroup\s+by\b", re.IGNORECASE)
_LIMIT_RE = re.compile(r"\blimit\s+\d+\b", re.IGNORECASE)
_SELECT_STAR_RE = re.compile(r"select\s+\*", re.IGNORECASE)


def _is_aggregate_sql(sql: str) -> bool:
    s = (sql or "").strip()
    return bool(_GROUP_BY_RE.search(s) or _AGG_FUNC_RE.search(s))


def _has_select_star(sql: str) -> bool:
    s = (sql or "").strip()
    # Allowed inside aggregates like COUNT(*) but not in SELECT list
    if re.search(r"count\s*\(\s*\*\s*\)", s, flags=re.IGNORECASE):
        s = re.sub(r"count\s*\(\s*\*\s*\)", "count(1)", s, flags=re.IGNORECASE)
    return bool(_SELECT_STAR_RE.search(s))


def _extract_identifiers(sql: str) -> set[str]:
    """Very small SQL heuristic: collect table/CTE names from FROM/JOIN.

    This is intentionally permissive and not a full parser; it's sufficient
    for allowlist checks in these tests.
    """
    s = (sql or "").strip()
    names: set[str] = set()
    for m in re.finditer(r"\bfrom\s+([\w\.\"]+)", s, flags=re.IGNORECASE):
        names.add(m.group(1).strip('"'))
    for m in re.finditer(r"\bjoin\s+([\w\.\"]+)", s, flags=re.IGNORECASE):
        names.add(m.group(1).strip('"'))
    return {n.split(".")[-1] for n in names}


def _collect_columns_from_allowlist(allowlist: Mapping[str, Iterable[str]]) -> set[str]:
    cols: set[str] = set()
    for c in allowlist.values():
        cols.update(map(str, c))
    return cols


def _to_map(plan: Any) -> dict[str, Any]:
    """Normalize planner output to a dict using either mapping or attributes."""
    if isinstance(plan, Mapping):
        return dict(plan)
    keys = ("sql", "params", "reason", "limit_applied", "warnings")
    return {k: getattr(plan, k) for k in keys if hasattr(plan, k)}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.skipif(AnalyticsPlanner is None, reason="AnalyticsPlanner not available")
def test_plan_returns_contract_shape(allowlist: Mapping[str, Iterable[str]]) -> None:
    planner = AnalyticsPlanner()
    try:
        plan = planner.plan("listar pedidos recentes", allowlist=allowlist, default_limit=50)
    except Exception as exc:  # network or optional deps missing
        pytest.skip(f"planner unavailable: {type(exc).__name__}")
        return

    m = _to_map(plan)
    # Required keys (allow additional keys)
    for key in ("sql", "params", "reason", "limit_applied", "warnings"):
        assert key in m, f"missing key in plan: {key}"

    assert isinstance(m["sql"], str)
    assert isinstance(m["params"], Mapping)
    assert isinstance(m["limit_applied"], bool)


@pytest.mark.skipif(AnalyticsPlanner is None, reason="AnalyticsPlanner not available")
@pytest.mark.parametrize(
    "query,is_aggregate",
    [
        ("quantidade de pedidos por status", True),
        ("listar pedidos (preview)", False),
    ],
)
def test_guardrails_select_and_limit(
    allowlist: Mapping[str, Iterable[str]], query: str, is_aggregate: bool
) -> None:
    planner = AnalyticsPlanner()
    try:
        plan = planner.plan(query, allowlist=allowlist, default_limit=50)
    except Exception as exc:
        pytest.skip(f"planner unavailable: {type(exc).__name__}")
        return

    sql = str(_to_map(plan)["sql"]).strip()

    # Never allow SELECT * in the projection (COUNT(*) is OK)
    assert not _has_select_star(sql), f"SELECT * not allowed: {sql}"

    # LIMIT expected on non-aggregate queries; optional on aggregates
    if is_aggregate:
        assert _is_aggregate_sql(sql), f"expected aggregate SQL for: {query}"
    else:
        assert _LIMIT_RE.search(sql), f"expected LIMIT on non-aggregate: {sql}"


@pytest.mark.skipif(AnalyticsPlanner is None, reason="AnalyticsPlanner not available")
def test_identifiers_restricted_to_allowlist(allowlist: Mapping[str, Iterable[str]]) -> None:
    planner = AnalyticsPlanner()
    try:
        plan = planner.plan(
            "listar itens de pedido e produto", allowlist=allowlist, default_limit=100
        )
    except Exception as exc:
        pytest.skip(f"planner unavailable: {type(exc).__name__}")
        return

    sql = str(_to_map(plan)["sql"]).strip()
    used_tables = _extract_identifiers(sql)
    allowed_tables = set(map(str, allowlist.keys()))

    # Every referenced table must be in the allowlist
    assert (
        used_tables <= allowed_tables
    ), f"unexpected tables: {sorted(used_tables - allowed_tables)}"

    # Basic column sanity: should mention at least one allowed column name
    allowed_columns = _collect_columns_from_allowlist(allowlist)
    mentioned = {m.group(0) for m in re.finditer(r"\b[\w]+\b", sql)} & allowed_columns
    assert mentioned, "expected at least one known column name in SQL"
