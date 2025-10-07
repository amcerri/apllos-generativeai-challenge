"""
Ingest Olist CSVs into PostgreSQL (analytics schema).

Overview
This script creates the analytics schema (via `schema.sql`) and bulk-loads the
Olist CSV datasets from `data/raw/analytics/` using PostgreSQL COPY for speed.
It is designed to be:
- **Idempotent**: safe to re-run; tables can be truncated first with a flag.
- **Dependency-light**: uses SQLAlchemy if available; falls back gracefully.
- **Strict about types**: relies on Postgres to coerce textual timestamps.

Design
1) Apply schema from a provided SQL file.
2) Discover known CSV filenames → target tables.
3) COPY rows with explicit column lists from CSV headers.
4) ANALYZE tables to refresh planner stats.

Integration
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

try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

# ---------------------------------------------------------------------------
# Optional SQLAlchemy engine (via infra or direct)
# ---------------------------------------------------------------------------
try:
    from sqlalchemy import create_engine as _create_engine
    from sqlalchemy.engine import Engine as _Engine

except Exception:  # pragma: no cover - optional
    _create_engine = None  # type: ignore[assignment]

try:
    from app.infra.db import get_engine as _get_engine  # preferred
except Exception:  # pragma: no cover - optional
    _get_engine = None  # type: ignore[assignment]

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

# Load order to satisfy foreign keys (lower comes first)
TABLE_ORDER: dict[str, int] = {
    "product_category_translation": 10,
    "products": 20,
    "customers": 30,
    "sellers": 40,
    "orders": 50,
    "order_items": 60,
    "order_payments": 70,
    "order_reviews": 80,
    "geolocation": 90,
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
        try:
            return _get_engine()
        except RuntimeError:
            # Fall back to DATABASE_URL if infra engine is not configured
            pass
    
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


def analyze_tables(engine: Any, tables: list[str]) -> None:
    if not tables:
        return
    with start_span("ingest.analyze", {"tables": ",".join(tables)}):
        with engine.begin() as conn:
            for t in tables:
                conn.exec_driver_sql(f"ANALYZE {_SCHEMA_NAME}.{t}")


def drop_fk_products_category_if_exists(engine: Any) -> None:
    """Drop products→translation FK if present (to allow loading mismatched CSVs)."""
    with start_span("ingest.drop_fk_products_category", None):
        with engine.begin() as conn:
            conn.exec_driver_sql(f"ALTER TABLE {_SCHEMA_NAME}.products DROP CONSTRAINT IF EXISTS fk_products_category")


def backfill_missing_product_categories(engine: Any) -> int:
    """Ensure translation has at least the categories present in products (self-translation)."""
    sql = f"""
    INSERT INTO {_SCHEMA_NAME}.product_category_translation
        (product_category_name, product_category_name_english)
    SELECT DISTINCT p.product_category_name, p.product_category_name
    FROM {_SCHEMA_NAME}.products AS p
    LEFT JOIN {_SCHEMA_NAME}.product_category_translation AS t
      ON t.product_category_name = p.product_category_name
    WHERE p.product_category_name IS NOT NULL
      AND t.product_category_name IS NULL
    """
    with start_span("ingest.backfill_categories", None):
        with engine.begin() as conn:
            res = conn.exec_driver_sql(sql)
            try:
                return int(getattr(res, "rowcount", 0))
            except Exception:
                return 0


def add_fk_products_category(engine: Any) -> None:
    """Recreate products→translation FK after backfilling."""
    with start_span("ingest.add_fk_products_category", None):
        with engine.begin() as conn:
            conn.exec_driver_sql(
                f"""
                ALTER TABLE {_SCHEMA_NAME}.products
                ADD CONSTRAINT fk_products_category
                FOREIGN KEY (product_category_name)
                REFERENCES {_SCHEMA_NAME}.product_category_translation(product_category_name)
                """
            )


def copy_csv(engine: Any, table: str, csv_path: Path) -> int:
    """COPY a CSV into a *temporary* table, then INSERT into analytics.table.

    This makes the ingestion idempotent by skipping rows that would violate
    primary key / unique constraints in the destination table.

    Strategy
    --------
    1) CREATE TEMP TABLE tmp_copy_<table> (LIKE analytics.<table> INCLUDING DEFAULTS) ON COMMIT DROP
       (no PK/unique constraints are copied, so duplicates load into temp).
    2) COPY the CSV into the temp table using server-side header handling.
    3) INSERT INTO analytics.<table> SELECT * FROM temp ON CONFLICT DO NOTHING.
       Return the number of inserted rows (not the number copied into temp).
    """
    temp_table = f"tmp_copy_{table}"
    schema_qualified = f"{_SCHEMA_NAME}.{table}"

    # COPY statement targets the temporary table (no explicit column list; rely on CSV header ↔ table columns)
    copy_sql = (
        f"COPY {temp_table} "
        "FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',', QUOTE '\"' , ESCAPE '\"', NULL '')"
    )

    insert_sql = f"INSERT INTO {schema_qualified} SELECT * FROM {temp_table} ON CONFLICT DO NOTHING"

    with start_span("ingest.copy_csv", {"table": table, "file": str(csv_path)}):
        raw = engine.raw_connection()
        try:
            cur: Any = raw.cursor()
            inserted_rows = -1
            try:
                # 1) Create the temp table shaped like the destination (no PK/unique constraints)
                cur.execute(
                    f"CREATE TEMP TABLE {temp_table} (LIKE {schema_qualified} INCLUDING DEFAULTS) ON COMMIT DROP"
                )

                # 2) COPY the CSV into the temp table
                if hasattr(cur, "copy"):
                    # psycopg3 streaming API expects bytes; stream file in chunks
                    with csv_path.open("rb") as fh:
                        with cur.copy(copy_sql) as cp:  # type: ignore[attr-defined]
                            while True:
                                chunk = fh.read(1024 * 1024)
                                if not chunk:
                                    break
                                cp.write(chunk)
                elif hasattr(cur, "copy_expert"):
                    # psycopg2 path; text mode works with HEADER TRUE
                    with csv_path.open("r", encoding="utf-8", newline="") as fh:
                        cur.copy_expert(copy_sql, fh)  # type: ignore[attr-defined]
                else:
                    raise RuntimeError(
                        "COPY not supported by DBAPI driver (expected cursor.copy or cursor.copy_expert)"
                    )

                # 3) Move data into the destination, skipping duplicates
                cur.execute(insert_sql)
                try:
                    inserted_rows = int(getattr(cur, "rowcount", -1))
                except Exception:
                    inserted_rows = -1

                raw.commit()
                return inserted_rows
            finally:
                try:
                    cur.close()
                except Exception:
                    pass
        finally:
            try:
                raw.close()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_files(data_dir: Path) -> list[tuple[str, Path]]:
    """Return a list of (table, path) for known CSVs found in data_dir, ordered to respect FKs."""
    found: list[tuple[str, Path]] = []
    for fname, table in CSV_TO_TABLE.items():
        p = data_dir / fname
        if p.exists():
            found.append((table, p))
    # Ensure product_category_translation loads before products, etc.
    found.sort(key=lambda pair: TABLE_ORDER.get(pair[0], 1000))
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
        schema_path=ns.schema_path,
        data_dir=ns.data_dir,
        truncate=ns.truncate,
        analyze=ns.analyze,
    )


def main(argv: list[str] | None = None) -> int:
    log = get_logger("scripts.ingest_analytics")
    opts = parse_args(argv)

    engine = _resolve_engine()

    with start_span("ingest.run", {"data_dir": str(opts.data_dir)}):
        # 1) Apply schema
        apply_schema(engine, opts.schema_path)
        drop_fk_products_category_if_exists(engine)

        # 2) Discover CSVs and target tables
        pairs = discover_files(opts.data_dir)
        if not pairs:
            log.warning("no csv files found", extra={"data_dir": str(opts.data_dir)})
            return 0

        tables = [t for t, _ in pairs]
        if opts.truncate:
            truncate_tables(engine, tables)

        # 3) Copy files
        total_rows = 0
        for table, path in pairs:
            rows = copy_csv(engine, table, path)
            total_rows += max(rows, 0)
            log.info("loaded csv", extra={"table": table, "path": str(path), "rows": rows})

        # Backfill any categories present in products but missing in translation, then re-add FK
        inserted = backfill_missing_product_categories(engine)
        log.info("category backfill complete", extra={"inserted": inserted})
        add_fk_products_category(engine)

        # 4) Analyze
        if opts.analyze:
            analyze_tables(engine, tables)

        log.info("ingest complete", extra={"files": len(pairs), "rows": total_rows})
        return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())