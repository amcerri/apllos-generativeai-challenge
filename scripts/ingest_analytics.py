"""
Ingest Olist CSVs into PostgreSQL (analytics schema).

Overview
--------
This script creates the analytics schema (via `schema.sql`) and bulk‑loads the
Olist CSV datasets from `data/raw/analytics/` using PostgreSQL COPY for speed.
It is designed to be:
- **Idempotent**: safe to re‑run; tables can be truncated first with a flag.
- **Dependency‑light**: uses SQLAlchemy if available; falls back gracefully.
- **Strict about types**: relies on Postgres to coerce textual timestamps.

Design
------
1) Apply schema from a provided SQL file.
2) Discover known CSV filenames → target tables.
3) COPY rows with explicit column lists from CSV headers.
4) ANALYZE tables to refresh planner stats.

Integration
-----------
- Expects `DATABASE_URL` (e.g., `postgresql+psycopg2://user:pass@host:5432/db`).
- Works with our infra helpers if present (`app.infra.db.get_engine`).
- Intended to be used locally and in CI as a smoke step.

Usage
-----
$ python -m scripts.ingest_analytics \
    --schema data/samples/schema.sql \
    --data-dir data/raw/analytics \
    --truncate --analyze

Environment
-----------
- DATABASE_URL (required unless engine is provided by `app.infra.db`).
"""

from __future__ import annotations

import argparse
import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional infra: logging and tracing fallbacks
# ---------------------------------------------------------------------------
try:
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - fallback
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
# Optional SQLAlchemy engine (via infra or direct)
# ---------------------------------------------------------------------------
_get_engine: Any = None
Engine: Any
try:
    from sqlalchemy import create_engine as _create_engine
    from sqlalchemy.engine import Engine as _Engine

    Engine = _Engine
except Exception:  # pragma: no cover - optional
    Engine = object  # sentinel type
    _create_engine = None

try:
    from app.infra.db import get_engine as _get_engine  # preferred
except Exception:  # pragma: no cover - optional
    _get_engine = None


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_DEFAULT_SCHEMA: Final[str] = "data/samples/schema.sql"
_DEFAULT_DATA_DIR: Final[str] = "data/raw/analytics"
_SCHEMA_NAME: Final[str] = "analytics"

# Known filename → table mapping (based on `olist_csv_files.txt`)
CSV_TO_TABLE: dict[str, str] = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "product_category_name_translation.csv": "product_category_translation",
}


@dataclass(slots=True)
class IngestOptions:
    schema_path: Path
    data_dir: Path
    truncate: bool
    analyze: bool


# ---------------------------------------------------------------------------
# Engine helpers
# ---------------------------------------------------------------------------


def _resolve_engine() -> Any:
    """Return a SQLAlchemy Engine using infra helper or DATABASE_URL.

    Raises a RuntimeError if neither helper nor env var is available.
    """
    if _get_engine is not None:
        return _get_engine()
    if _create_engine is None:
        raise RuntimeError("SQLAlchemy is required but not available")
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set and infra.get_engine is unavailable")
    return _create_engine(url, pool_pre_ping=True, future=True)


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------


def apply_schema(engine: Any, schema_path: Path) -> None:
    """Execute the schema SQL file (multiple statements allowed)."""
    sql_text = schema_path.read_text(encoding="utf-8")
    with start_span("ingest.apply_schema", {"path": str(schema_path)}):
        with engine.begin() as conn:
            # exec_driver_sql allows multiple statements in one call in PG
            conn.exec_driver_sql(sql_text)


def truncate_tables(engine: Any, tables: list[str]) -> None:
    if not tables:
        return
    with start_span("ingest.truncate", {"tables": ",".join(tables)}):
        with engine.begin() as conn:
            table_list = ", ".join(f"{_SCHEMA_NAME}.{t}" for t in tables)
            conn.exec_driver_sql(f"TRUNCATE {table_list} RESTART IDENTITY CASCADE")


def _read_csv_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        return [h.strip() for h in header]


def copy_csv(engine: Any, table: str, csv_path: Path) -> int:
    """COPY a CSV file into `analytics.table` using the header as column list.

    Returns the number of rows ingested (best effort; relies on driver rowcount
    when available, otherwise returns -1).
    """
    columns = _read_csv_header(csv_path)
    col_list = ", ".join(columns)
    copy_sql = (
        f"COPY {_SCHEMA_NAME}.{table} ({col_list}) "
        "FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',', QUOTE '\"' , ESCAPE '\"', NULL '')"
    )

    # Use raw DBAPI connection to access copy_expert (psycopg2/psycopg)
    with start_span("ingest.copy_csv", {"table": table, "file": str(csv_path)}):
        with engine.raw_connection() as raw:
            cur = raw.cursor()
            with csv_path.open("r", encoding="utf-8", newline="") as fh:
                try:
                    # psycopg2/psycopg both expose copy_expert
                    cur.copy_expert(copy_sql, fh)
                finally:
                    raw.commit()
            try:
                return int(getattr(cur, "rowcount", -1))
            except Exception:
                return -1


def analyze_tables(engine: Any, tables: list[str]) -> None:
    if not tables:
        return
    with start_span("ingest.analyze", {"tables": ",".join(tables)}):
        with engine.begin() as conn:
            for t in tables:
                conn.exec_driver_sql(f"ANALYZE {_SCHEMA_NAME}.{t}")


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def discover_files(data_dir: Path) -> list[tuple[str, Path]]:
    """Return a list of (table, path) for known CSVs found in data_dir."""
    found: list[tuple[str, Path]] = []
    for fname, table in CSV_TO_TABLE.items():
        p = data_dir / fname
        if p.exists():
            found.append((table, p))
    return found


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> IngestOptions:
    ap = argparse.ArgumentParser(description="Ingest Olist CSVs into analytics schema")
    ap.add_argument("--schema", dest="schema_path", default=_DEFAULT_SCHEMA, type=Path)
    ap.add_argument("--data-dir", dest="data_dir", default=_DEFAULT_DATA_DIR, type=Path)
    ap.add_argument("--truncate", action="store_true", help="TRUNCATE tables before loading")
    ap.add_argument("--analyze", action="store_true", help="Run ANALYZE after load")
    ns = ap.parse_args(argv)
    return IngestOptions(
        schema_path=ns.schema_path, data_dir=ns.data_dir, truncate=ns.truncate, analyze=ns.analyze
    )


def main(argv: list[str] | None = None) -> int:
    log = get_logger("scripts.ingest_analytics")
    opts = parse_args(argv)

    engine = _resolve_engine()

    with start_span("ingest.run", {"data_dir": str(opts.data_dir)}):
        # 1) Apply schema
        apply_schema(engine, opts.schema_path)

        # 2) Discover CSVs and target tables
        pairs = discover_files(opts.data_dir)
        if not pairs:
            log.warning("no csv files found", data_dir=str(opts.data_dir))
            return 0

        tables = [t for t, _ in pairs]
        if opts.truncate:
            truncate_tables(engine, tables)

        # 3) Copy files
        total_rows = 0
        for table, path in pairs:
            rows = copy_csv(engine, table, path)
            total_rows += max(rows, 0)
            log.info("loaded csv", table=table, path=str(path), rows=rows)

        # 4) Analyze
        if opts.analyze:
            analyze_tables(engine, tables)

        log.info("ingest complete", files=len(pairs), rows=total_rows)
        return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
