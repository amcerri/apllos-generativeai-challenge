"""
Analytics normalizer (business-friendly Portuguese narration).

Overview
--------
Convert the raw rows produced by the analytics executor into a user-facing
`Answer` object (or plain mapping) with:
- Natural PT‑BR narrative (`text`) tailored to the query shape (count,
  time series, preview/top‑N).
- Optional tabular payload (`data`, `columns`).
- Diagnostics in `meta` (SQL, row_count, limit flags, timings).

Design
------
- Pure Python (no third‑party deps), type‑annotated and lint‑friendly.
- Shape inference by inspecting output columns (e.g., `period`, `qty`).
- Conservative formatting: locale‑like number formatting for PT‑BR and
  ISO‑like dates for data payload stability.

Integration
-----------
- Called by the analytics agent after executing the planner SQL.
- Accepts a `plan` (dict‑like with `sql`, `limit_applied`) and a `result`
  (dict‑like with `rows`, `row_count`, `exec_ms`, `limit_applied`).
- Returns a dataclass `Answer` if available; else a plain `dict` with the
  same fields.

Usage
-----
>>> from app.agents.analytics.normalize import AnalyticsNormalizer
>>> norm = AnalyticsNormalizer()
>>> ans = norm.normalize(
...     plan={"sql": "SELECT COUNT(1) AS qty FROM orders", "limit_applied": False},
...     result={"rows": [{"qty": 42}], "row_count": 1, "exec_ms": 3.2, "limit_applied": False},
...     question="Quantos pedidos existem?",
... )
>>> isinstance(ans, dict) or hasattr(ans, "text")
True
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Final, cast

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


# Tracing (optional; keep a single alias)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# Optional Answer dataclass
ANSWER_CLS: Any
try:
    from app.contracts.answer import Answer as _Answer

    ANSWER_CLS = _Answer
except Exception:  # pragma: no cover - optional
    ANSWER_CLS = None

__all__ = ["AnalyticsNormalizer"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class _PlanView:
    sql: str
    limit_applied: bool


@dataclass(slots=True)
class _ResultView:
    rows: list[Mapping[str, Any]]
    row_count: int
    exec_ms: float
    limit_applied: bool


class AnalyticsNormalizer:
    """Produce a PT‑BR narrative and tabular payload from executor results."""

    MAX_PREVIEW_ROWS: Final[int] = 500  # additional safety for payload size

    def __init__(self) -> None:
        self.log = get_logger("agent.analytics.normalize")

    def normalize(
        self,
        *,
        plan: Mapping[str, Any] | _PlanView,
        result: Mapping[str, Any] | _ResultView,
        question: str | None = None,
    ) -> Any:
        """Return an Answer‑like object with PT‑BR text and optional table.

        Parameters
        ----------
        plan: Dict or object with `sql`, `limit_applied`.
        result: Dict or object with `rows`, `row_count`, `exec_ms`, `limit_applied`.
        question: Original user question (optional; used for tone/hints).
        """

        with start_span("agent.analytics.normalize"):
            p = _as_plan(plan)
            r = _as_result(result)

            rows_raw = list(r.rows)
            columns = _infer_columns(rows_raw)

            shape = _infer_shape(columns)
            table = _extract_table_from_sql(p.sql)
            scale = _extract_timescale_from_sql(p.sql)

            if shape == "count":
                text = _render_count_ptbr(rows_raw, table)
                data, cols = None, None
            elif shape == "timeseries":
                text = _render_timeseries_ptbr(rows_raw, table, scale)
                data, cols = _limit_rows(rows_raw, self.MAX_PREVIEW_ROWS), columns
            else:  # preview
                text = _render_preview_ptbr(rows_raw, table, r.row_count, p.limit_applied)
                data, cols = _limit_rows(rows_raw, self.MAX_PREVIEW_ROWS), columns

            meta = {
                "sql": p.sql,
                "row_count": r.row_count,
                "limit_applied": bool(p.limit_applied or r.limit_applied),
                "exec_ms": r.exec_ms,
            }

            followups = _suggest_followups(shape, table)

            payload = {
                "text": text,
                **(
                    {"data": data, "columns": cols} if data is not None and cols is not None else {}
                ),
                "meta": meta,
                "followups": followups,
            }
            return _coerce_answer(payload)


# ---------------------------------------------------------------------------
# Shape detection & rendering
# ---------------------------------------------------------------------------


def _infer_columns(rows: list[Mapping[str, Any]]) -> list[str]:
    if not rows:
        return []
    # Preserve insertion order of the first row
    return [str(k) for k in rows[0].keys()]


def _infer_shape(columns: list[str]) -> str:
    cols = {c.lower() for c in columns}
    if {"qty"} == cols or ("qty" in cols and len(cols) == 1):
        return "count"
    if {"period", "qty"}.issubset(cols):
        return "timeseries"
    return "preview"


def _render_count_ptbr(rows: list[Mapping[str, Any]], table: str | None) -> str:
    qty = 0
    if rows and isinstance(rows[0].get("qty"), int | float):
        qty = (
            int(rows[0]["qty"])
            if not isinstance(rows[0]["qty"], float)
            else int(round(rows[0]["qty"]))
        )
    qfmt = _fmt_int_ptbr(qty)
    alvo = f" na tabela `{table}`" if table else ""
    return f"Encontrei {qfmt} registros{alvo}."


def _render_timeseries_ptbr(
    rows: list[Mapping[str, Any]], table: str | None, scale: str | None
) -> str:
    if not rows:
        alvo = f" na tabela `{table}`" if table else ""
        return f"Não encontrei dados de série temporal{alvo}."
    total = sum(int(r.get("qty", 0) or 0) for r in rows)
    qfmt = _fmt_int_ptbr(total)
    nper = len(rows)
    escala = {"month": "mensal", "week": "semanal", "day": "diária", "year": "anual"}.get(
        scale or "", "temporal"
    )
    alvo = f" na tabela `{table}`" if table else ""
    # Últimos 3 pontos, se houver
    tail = rows[-3:]
    tail_str = ", ".join(
        f"{_fmt_period_ptbr(r.get('period'))}: {_fmt_int_ptbr(int(r.get('qty', 0) or 0))}"
        for r in tail
    )
    return (
        f"Série {escala}{alvo}: {qfmt} ocorrências em {nper} períodos. "
        f"Últimos pontos: {tail_str}."
    )


def _render_preview_ptbr(
    rows: list[Mapping[str, Any]],
    table: str | None,
    row_count: int,
    limit_applied: bool,
) -> str:
    if not rows:
        alvo = f" na tabela `{table}`" if table else ""
        return f"Não há linhas para exibir{alvo}."
    shown = len(rows)
    alvo = f" da tabela `{table}`" if table else ""
    if limit_applied:
        return f"Mostrando {shown} linhas{alvo} (cap de segurança). Refine o filtro para mais detalhes."
    return f"Mostrando {shown} linhas{alvo}."


# ---------------------------------------------------------------------------
# Extractors & formatting helpers
# ---------------------------------------------------------------------------


def _as_plan(obj: Mapping[str, Any] | _PlanView) -> _PlanView:
    if isinstance(obj, Mapping):
        return _PlanView(
            sql=str(obj.get("sql", "")), limit_applied=bool(obj.get("limit_applied", False))
        )
    return obj


def _as_result(obj: Mapping[str, Any] | _ResultView) -> _ResultView:
    if isinstance(obj, Mapping):
        rows_any = list(obj.get("rows", []) or [])
        rows: list[Mapping[str, Any]] = [cast(Mapping[str, Any], r) for r in rows_any]
        return _ResultView(
            rows=rows,
            row_count=int(obj.get("row_count", len(rows))),
            exec_ms=float(obj.get("exec_ms", 0.0)),
            limit_applied=bool(obj.get("limit_applied", False)),
        )
    return obj


def _coerce_answer(dec: Mapping[str, Any]) -> Any:
    if ANSWER_CLS is None:
        return dict(dec)
    try:
        if hasattr(ANSWER_CLS, "from_dict"):
            return ANSWER_CLS.from_dict(dec)
        if hasattr(ANSWER_CLS, "from_mapping"):
            return ANSWER_CLS.from_mapping(dec)
        return ANSWER_CLS(**dec)
    except Exception:
        return dict(dec)


def _extract_table_from_sql(sql: str) -> str | None:
    m = re.search(r"\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)\b", sql, flags=re.IGNORECASE)
    return m.group(1) if m else None


def _extract_timescale_from_sql(sql: str) -> str | None:
    m = re.search(r"date_trunc\('([a-zA-Z]+)'", sql, flags=re.IGNORECASE)
    return m.group(1).lower() if m else None


def _limit_rows(rows: list[Mapping[str, Any]], cap: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for r in rows[:cap]:
        out.append({k: _coerce_primitive(v) for k, v in r.items()})
    return out


def _coerce_primitive(v: Any) -> Any:
    if isinstance(v, int | float | str) or v is None:
        return v
    if isinstance(v, datetime | date):
        return v.isoformat()
    # SQLAlchemy Decimal / UUID / others → try best‑effort str
    try:
        return float(v) if hasattr(v, "as_integer_ratio") or isinstance(v, int | float) else str(v)
    except Exception:
        return str(v)


def _fmt_int_ptbr(n: int) -> str:
    s = f"{n:,}"
    return s.replace(",", ".")


def _fmt_float_ptbr(x: float, digits: int = 2) -> str:
    if math.isnan(x) or math.isinf(x):
        return str(x)
    s = f"{x:,.{digits}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def _fmt_period_ptbr(v: Any) -> str:
    if isinstance(v, datetime | date):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, str):
        # try to shorten YYYY-MM-DDTHH:MM:SS
        m = re.match(r"(\d{4}-\d{2}-\d{2})", v)
        if m:
            return m.group(1)
        return v
    return str(v)


def _suggest_followups(shape: str, table: str | None) -> list[str]:
    if shape == "count":
        base = f"{table} " if table else ""
        return [
            f"Quer ver a evolução mensal de {base}?",
            f"Deseja detalhar por status em {base}?",
        ]
    if shape == "timeseries":
        base = f"{table} " if table else ""
        return [
            f"Filtrar a série por status ou categoria em {base}?",
            f"Comparar períodos (YoY/MoM) em {base}?",
        ]
    # preview
    base = f"{table} " if table else ""
    return [
        f"Adicionar filtros (ex.: data, status) em {base}?",
        f"Agregarmos por mês ou por vendedor em {base}?",
    ]
