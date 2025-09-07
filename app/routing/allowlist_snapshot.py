"""
Allowlist snapshot (tables → columns) for analytics routing and planning.

Overview
    Provides a small, dependency‑light registry for allowed tables/columns used
    by the router and the analytics SQL planner. Supports three usage modes:
    (1) in‑memory snapshot (set at runtime), (2) JSON serialization, and
    (3) optional DB introspection (Postgres via SQLAlchemy engine) to bootstrap
    the snapshot from an existing schema.

Design
    - Keep the contract simple: mapping[str, list[str]] (table → sorted columns).
    - No hard dependency on SQLAlchemy or internal DB modules; introspection is
      optional and performed only on demand.
    - Pure functions with explicit types; global, replaceable snapshot.

Integration
    - Router: inject `allowlist_json()` into routing prompts for table/column
      extraction.
    - Planner: validate candidate SQL identifiers against `get_snapshot()`.
    - Scripts: `scripts/gen_allowlist.py` can call `refresh_from_db(...)` and
      persist to a file for reproducible runs.

Usage
    >>> from app.routing.allowlist_snapshot import set_snapshot, get_snapshot, allowlist_json
    >>> set_snapshot({"orders": ["order_id", "order_status"]})
    >>> get_snapshot()["orders"]
    ['order_id', 'order_status']
    >>> allowlist_json()
    '{"orders": ["order_id", "order_status"]}'
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

# Internal, replaceable snapshot. Keys: table names; Values: sorted list of columns.
_SNAPSHOT: dict[str, list[str]] = {}


# ---------------------------------------------------------------------------
# Public API — snapshot management
# ---------------------------------------------------------------------------


def set_snapshot(mapping: Mapping[str, Iterable[str]]) -> None:
    """Replace the global allowlist snapshot with a validated copy.

    - Table and column names are normalized to strings and stripped.
    - Column lists are sorted and de‑duplicated.
    """

    global _SNAPSHOT
    snap: dict[str, list[str]] = {}
    for raw_table, raw_cols in mapping.items():
        table = str(raw_table).strip()
        if not table:
            continue
        cols: list[str] = []
        seen: set[str] = set()
        for c in raw_cols:
            col = str(c).strip()
            if not col or col in seen:
                continue
            seen.add(col)
            cols.append(col)
        cols.sort()
        snap[table] = cols
    _SNAPSHOT = dict(sorted(snap.items(), key=lambda kv: kv[0]))


def get_snapshot() -> dict[str, list[str]]:
    """Return a copy of the current snapshot (table → columns)."""

    return {t: list(cols) for t, cols in _SNAPSHOT.items()}


def add_table(table: str, columns: Iterable[str]) -> None:
    """Add or replace a table entry in the snapshot."""

    t = str(table).strip()
    cols = sorted({str(c).strip() for c in columns if str(c).strip()})
    if not t:
        return
    _SNAPSHOT[t] = cols


def is_allowed_table(table: str) -> bool:
    """Return True if *table* exists in the snapshot."""

    return str(table).strip() in _SNAPSHOT


def is_allowed_column(table: str, column: str) -> bool:
    """Return True if *column* exists under *table* in the snapshot."""

    t = str(table).strip()
    c = str(column).strip()
    return bool(t and c and (t in _SNAPSHOT) and (c in _SNAPSHOT[t]))


def allowlist_json(compact: bool = True) -> str:
    """Return the snapshot as a JSON string (sorted for determinism)."""

    if compact:
        return json.dumps(_SNAPSHOT, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return json.dumps(_SNAPSHOT, ensure_ascii=False, sort_keys=True, indent=2)


# ---------------------------------------------------------------------------
# Optional: DB introspection (Postgres/SQLAlchemy engine)
# ---------------------------------------------------------------------------


def load_from_engine(engine: Any, *, schema: str = "public") -> dict[str, list[str]]:
    """Return an allowlist mapping by introspecting INFORMATION_SCHEMA.

    Parameters
    ----------
    engine: SQLAlchemy engine or conn‑compatible object exposing `.connect()`.
    schema: Database schema to inspect (default: "public").
    """

    query = (
        "SELECT table_name, column_name "
        "FROM information_schema.columns "
        "WHERE table_schema = :schema "
        "ORDER BY table_name, ordinal_position"
    )

    out: dict[str, list[str]] = {}
    with engine.connect() as conn:
        rows = conn.exec_driver_sql(query, {"schema": schema}).all()
    for table, column in rows:
        out.setdefault(str(table), []).append(str(column))
    for t in list(out.keys()):
        out[t] = sorted({c.strip() for c in out[t] if str(c).strip()})
    return dict(sorted(out.items(), key=lambda kv: kv[0]))


def refresh_from_db(*, schema: str = "public") -> dict[str, list[str]]:
    """Replace the global snapshot using the configured engine, if available.

    Tries to import `app.infra.db.get_engine()` lazily to avoid hard deps. Raises
    `RuntimeError` if the engine is not configured.
    """

    try:
        from app.infra.db import get_engine  # import locally to keep optional dep
    except Exception as exc:  # pragma: no cover - optional path
        raise RuntimeError("database engine accessor not available") from exc

    eng = get_engine()
    snap = load_from_engine(eng, schema=schema)
    set_snapshot(snap)
    return get_snapshot()
