"""
Generate allowlist (tables → columns) from PostgreSQL introspection.

Overview
--------
This utility inspects a PostgreSQL schema (default: `analytics`) and emits a
JSON allowlist mapping each table name to the list of column names. The file is
used by the Analytics agent planner to constrain SQL generation to known tables
and columns.

Design
------
- Read-only introspection via information_schema.
- Optional inclusion of views; base tables only by default.
- Deterministic output: sorted tables and columns.
- Minimal dependencies; integrates with our infra helpers if present.

Integration
-----------
- Uses `app.infra.db.get_engine()` when available; otherwise falls back to
  `DATABASE_URL` with SQLAlchemy.
- Intended to be committed under `data/samples/allowlist.json` (default path),
  but the `--out` flag can be used to override.

Usage
-----
$ python -m scripts.gen_allowlist \
    --schema analytics \
    --out data/samples/allowlist.json \
    --include-views
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional infra: logging & tracing (safe fallbacks)
# ---------------------------------------------------------------------------
try:
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - simple fallback
        return _logging.getLogger(component)


start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# ---------------------------------------------------------------------------
# Optional SQLAlchemy engine (via infra or env)
# ---------------------------------------------------------------------------
_get_engine: Any = None

Engine: Any
try:
    from sqlalchemy import create_engine as _create_engine
    from sqlalchemy import text as _sql_text, bindparam as _bindparam
    from sqlalchemy.engine import Engine as _Engine

    Engine = _Engine
except Exception:  # pragma: no cover - optional
    Engine = object  # sentinel
    _create_engine = None
    _sql_text = None

try:
    from app.infra.db import get_engine as _get_engine
except Exception:  # pragma: no cover - optional
    pass


# ---------------------------------------------------------------------------
# Constants & dataclasses
# ---------------------------------------------------------------------------
_DEFAULT_SCHEMA: Final[str] = "analytics"
_DEFAULT_OUT: Final[str] = "data/samples/allowlist.json"


@dataclass(slots=True)
class GenOptions:
    schema: str
    include_views: bool
    out_path: Path


# ---------------------------------------------------------------------------
# Engine & core logic
# ---------------------------------------------------------------------------


def _resolve_engine() -> Any:
    if _get_engine is not None:
        return _get_engine()
    if _create_engine is None:
        raise RuntimeError("SQLAlchemy is required but not available")
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set and infra.get_engine is unavailable")
    return _create_engine(url, pool_pre_ping=True, future=True)


def _fetch_allowlist(engine: Any, *, schema: str, include_views: bool) -> dict[str, list[str]]:
    """Return mapping table → sorted list of columns from information_schema."""
    # Restrict to base tables by default; optionally include views
    kinds = ("BASE TABLE", "VIEW") if include_views else ("BASE TABLE",)

    out: dict[str, list[str]] = {}
    with engine.begin() as conn:
        if _sql_text is not None:
            sql = """
                SELECT c.table_name, c.column_name
                FROM information_schema.columns c
                JOIN information_schema.tables t
                  ON t.table_schema = c.table_schema AND t.table_name = c.table_name
                WHERE c.table_schema = :schema
                  AND t.table_type IN :kinds
                  AND c.table_name NOT LIKE 'pg\\_%' ESCAPE '\\'
                  AND c.table_name NOT LIKE 'sql\\_%' ESCAPE '\\'
                ORDER BY c.table_name, c.ordinal_position
            """
            stmt = _sql_text(sql).bindparams(_bindparam("kinds", expanding=True))
            res = conn.execute(stmt, {"schema": schema, "kinds": list(kinds)})
        else:
            # Fallback for DBAPI pathways without SQLAlchemy text/expanding params
            type_filter = "IN ('BASE TABLE','VIEW')" if include_views else "= 'BASE TABLE'"
            sql = f"""
                SELECT c.table_name, c.column_name
                FROM information_schema.columns c
                JOIN information_schema.tables t
                  ON t.table_schema = c.table_schema AND t.table_name = c.table_name
                WHERE c.table_schema = :schema
                  AND t.table_type {type_filter}
                  AND c.table_name NOT LIKE 'pg\\_%' ESCAPE '\\'
                  AND c.table_name NOT LIKE 'sql\\_%' ESCAPE '\\'
                ORDER BY c.table_name, c.ordinal_position
            """
            res = conn.exec_driver_sql(sql, {"schema": schema})
        for table, column in res.fetchall():
            out.setdefault(str(table), []).append(str(column))

    # Deduplicate and sort defensively
    return {t: sorted(dict.fromkeys(cols)) for t, cols in out.items()}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> GenOptions:
    ap = argparse.ArgumentParser(description="Generate allowlist (tables→columns) from Postgres")
    ap.add_argument("--schema", default=_DEFAULT_SCHEMA)
    ap.add_argument("--out", dest="out_path", type=Path, default=Path(_DEFAULT_OUT))
    ap.add_argument("--include-views", action="store_true")
    ns = ap.parse_args(argv)
    return GenOptions(
        schema=str(ns.schema), include_views=bool(ns.include_views), out_path=ns.out_path
    )


def main(argv: list[str] | None = None) -> int:
    log = get_logger("scripts.gen_allowlist")
    opts = parse_args(argv)

    engine = _resolve_engine()

    with start_span(
        "allowlist.generate", {"schema": opts.schema, "include_views": opts.include_views}
    ):
        allowlist = _fetch_allowlist(engine, schema=opts.schema, include_views=opts.include_views)

    # Ensure parent folder exists
    opts.out_path.parent.mkdir(parents=True, exist_ok=True)
    opts.out_path.write_text(
        json.dumps(allowlist, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    log.info("allowlist written", path=str(opts.out_path), tables=len(allowlist))
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
