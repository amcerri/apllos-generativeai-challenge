"""
Explain SQL plans against PostgreSQL (EXPLAIN / EXPLAIN ANALYZE).

Overview
Developer utility to inspect query plans safely. It connects to Postgres,
wraps the provided SQL in `EXPLAIN (...)` with configurable options, and
returns the plan in JSON or text. The script is conservative: it only allows
`SELECT`/`WITH` statements and refuses anything that looks like DML/DDL.

Design
- Optional dependency on our infra (`app.infra.db.get_engine`) with fallback to
  `DATABASE_URL` using SQLAlchemy.
- Minimal SQL validation (read‑only, no multi‑statement, optional basic allowlist).
- Robust CLI with JSON/text output and optional file write.

Integration
- Requires access to a PostgreSQL instance with the analytics/knowledge data.
- Use this during dev/CI to inspect performance or verify planner choices.

Usage
$ python -m scripts.explain_sql \
    --sql "SELECT count(*) FROM analytics.orders" \
    --analyze --buffers --format json --out plan.json

$ python -m scripts.explain_sql \
    --sql-file query.sql --params '{"status": "delivered"}' --format text
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional infra: logging & tracing with safe fallbacks
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
    from sqlalchemy import text as _sql_text
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
_TRUE_SET: Final[set[str]] = {"1", "true", "yes", "on"}


@dataclass(slots=True)
class ExplainOptions:
    sql: str
    params: dict[str, Any]
    analyze: bool
    buffers: bool
    verbose: bool
    timing: bool
    fmt: str  # "json" | "text"
    out_path: Path | None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _as_bool(v: Any, default: bool) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    s = str(v).strip().lower()
    if s in _TRUE_SET:
        return True
    if s in {"0", "false", "no", "off"}:
        return False
    return default


def _read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


_SELECT_RE = re.compile(r"^\s*(select|with)\b", re.IGNORECASE | re.DOTALL)
_SEMI_RE = re.compile(r";+")


def is_safe_select(sql: str) -> tuple[bool, str | None]:
    """Heuristic checks to ensure read-only, single-statement select/cte."""
    s = (sql or "").strip()
    if not s:
        return False, "empty SQL"
    if not _SELECT_RE.match(s):
        return False, "only SELECT/WITH statements are allowed"
    # Refuse multiple statements; allow a single trailing semicolon only
    semis = _SEMI_RE.findall(s)
    if len(semis) > 1 or (len(semis) == 1 and not s.endswith(";")):
        return False, "multiple statements are not allowed"
    # Very naive DML keywords defense-in-depth
    lowered = s.lower()
    if any(
        kw in lowered
        for kw in (" insert ", " update ", " delete ", " alter ", " drop ", " create ")
    ):
        return False, "detected non-read-only keywords"
    return True, None


def _resolve_engine() -> Any:
    if _get_engine is not None:
        return _get_engine()
    if _create_engine is None:
        raise RuntimeError("SQLAlchemy is required but not available")
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set and infra.get_engine is unavailable")
    return _create_engine(url, pool_pre_ping=True, future=True)


def build_explain_prefix(
    *, analyze: bool, buffers: bool, verbose: bool, timing: bool, fmt: str
) -> str:
    opts: list[str] = []
    if fmt == "json":
        opts.append("FORMAT JSON")
    if analyze:
        opts.append("ANALYZE TRUE")
    if buffers:
        opts.append("BUFFERS TRUE")
    if verbose:
        opts.append("VERBOSE TRUE")
    if timing:
        opts.append("TIMING TRUE")
    inner = ", ".join(opts) if opts else ""
    return f"EXPLAIN ({inner})" if inner else "EXPLAIN"


def run_explain(engine: Any, opts: ExplainOptions) -> dict[str, Any]:
    """Execute EXPLAIN over the given SQL and return a structured plan.

    For `fmt=json`, return the parsed JSON structure (first row/first cell).
    For `fmt=text`, return a dict with a `text` field containing the lines.
    """
    safe, reason = is_safe_select(opts.sql)
    if not safe:
        raise ValueError(f"unsafe SQL: {reason}")

    prefix = build_explain_prefix(
        analyze=opts.analyze,
        buffers=opts.buffers,
        verbose=opts.verbose,
        timing=opts.timing,
        fmt=opts.fmt,
    )

    explain_sql = f"{prefix} {opts.sql.strip().rstrip(';')}"

    with start_span("explain.run", {"format": opts.fmt, "analyze": opts.analyze}):
        with engine.begin() as conn:
            if _sql_text is None:
                # Very old SQLAlchemy: fallback to driver SQL
                res = conn.exec_driver_sql(explain_sql, opts.params)
            else:
                res = conn.execute(_sql_text(explain_sql), opts.params)

            rows = res.fetchall()
            if opts.fmt == "json":
                # First row, first column contains a JSON array
                raw = rows[0][0]
                payload = raw[0] if isinstance(raw, list) else raw
                if isinstance(payload, bytes | bytearray):
                    payload = json.loads(payload.decode("utf-8"))
                elif isinstance(payload, str):
                    payload = json.loads(payload)
                assert isinstance(payload, Mapping)
                return {"plan": payload}
            else:
                # Text format returns one line per row under column 'QUERY PLAN'
                lines = [str(r[0]) for r in rows]
                return {"text": "\n".join(lines)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> ExplainOptions:
    ap = argparse.ArgumentParser(description="EXPLAIN (ANALYZE) helper for PostgreSQL")

    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sql", dest="sql", type=str, help="SQL text (SELECT/WITH only)")
    src.add_argument("--sql-file", dest="sql_file", type=Path, help="Path to a .sql file")

    ap.add_argument(
        "--params", dest="params", type=str, default=None, help="JSON dict of bind parameters"
    )
    ap.add_argument(
        "--params-file",
        dest="params_file",
        type=Path,
        default=None,
        help="Path to JSON params file",
    )

    ap.add_argument(
        "--analyze", action="store_true", help="Run EXPLAIN ANALYZE (executes the query)"
    )
    ap.add_argument("--buffers", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--timing", action="store_true")
    ap.add_argument("--format", dest="fmt", choices=["json", "text"], default="json")
    ap.add_argument("--out", dest="out_path", type=Path, default=None)

    ns = ap.parse_args(argv)

    if ns.sql_file is not None:
        sql = _read_file(ns.sql_file)
    else:
        sql = ns.sql

    params: dict[str, Any] = {}
    if ns.params_file is not None:
        params = json.loads(_read_file(ns.params_file))
    elif ns.params is not None:
        params = json.loads(ns.params)

    return ExplainOptions(
        sql=sql,
        params=params,
        analyze=bool(ns.analyze),
        buffers=bool(ns.buffers),
        verbose=bool(ns.verbose),
        timing=bool(ns.timing),
        fmt=ns.fmt,
        out_path=ns.out_path,
    )


def main(argv: list[str] | None = None) -> int:
    log = get_logger("scripts.explain_sql")
    opts = parse_args(argv)

    try:
        engine = _resolve_engine()
    except Exception as exc:
        log.exception("db engine failure", extra={"error": type(exc).__name__})
        return 3

    try:
        result = run_explain(engine, opts)
    except Exception as exc:
        log.exception("explain failed", extra={"error": type(exc).__name__})
        return 2

    # Output: either write to file or log a concise summary
    if opts.out_path is not None:
        payload = result.get("plan") if opts.fmt == "json" else result
        opts.out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        log.info("wrote plan", extra={"path": str(opts.out_path), "format": opts.fmt})
    else:
        # Text summary for console via logger (avoids print)
        if opts.fmt == "json":
            try:
                # Compact JSON in one line to keep logs concise
                log.info("plan", extra={"payload": json.dumps(result.get("plan"), ensure_ascii=False)})
            except Exception:
                log.info("plan-json-bytes")
        else:
            log.info("plan-text\n" + result["text"])  # one multi-line log record

    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
