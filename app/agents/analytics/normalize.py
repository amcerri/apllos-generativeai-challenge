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

            # Enhanced context-aware rendering
            text = _render_intelligent_response(rows_raw, p.sql, table, shape, scale, r.row_count, p.limit_applied)
            
            if shape == "count":
                data, cols = None, None
            elif shape == "timeseries":
                data, cols = _limit_rows(rows_raw, self.MAX_PREVIEW_ROWS), columns
            else:  # preview
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
    # Check for distribution patterns (grouping column + count column)
    if any(col in columns for col in ['customer_state', 'product_category_name', 'seller_state']):
        if any(keyword in col.lower() for col in columns for keyword in ['count', 'qty', 'total']):
            return "distribution"
    return "preview"


def _render_intelligent_response(
    rows: list[Mapping[str, Any]], 
    sql: str, 
    table: str | None, 
    shape: str, 
    scale: str | None, 
    row_count: int, 
    limit_applied: bool,
    user_query: str = ""
) -> str:
    """Generate intelligent, context-aware response based on SQL and data."""
    
    if not rows:
        return "Não foram encontrados dados para sua consulta."
    
    sql_lower = sql.lower()
    first_row = rows[0]
    columns = list(first_row.keys())
    
    # Detect revenue/financial queries
    if any(keyword in sql_lower for keyword in ['sum(', 'price', 'freight_value', 'payment_value']):
        if 'customer_state' in columns:
            total_revenue = sum(_as_float(row.get('receita', 0)) for row in rows)
            top_state = rows[0].get('customer_state', 'N/A')
            top_revenue = _as_float(rows[0].get('receita', 0))
            return f"A receita total é R$ {_fmt_float_ptbr(total_revenue)}. O estado com maior receita é {top_state} (R$ {_fmt_float_ptbr(top_revenue)})."
        
        elif len(rows) == 1 and any(col in columns for col in ['total_revenue', 'receita']):
            revenue = _as_float(list(first_row.values())[0])
            return f"A receita total é R$ {_fmt_float_ptbr(revenue)}."
    
    # Detect filtered order queries (e.g., undelivered orders)
    if 'order_id' in columns and any(keyword in sql_lower for keyword in ['where', '<>', '!=', 'not']):
        if 'delivered' in sql_lower:
            if row_count == 0:
                return "Todos os pedidos já foram entregues."
            else:
                return f"Encontrei {_fmt_int_ptbr(row_count)} pedidos que ainda não foram entregues."
        elif any(status in sql_lower for status in ['shipped', 'processing', 'cancelled']):
            return f"Encontrei {_fmt_int_ptbr(row_count)} pedidos com esse status."
    
    # Detect status distribution queries (check this BEFORE general count queries)
    if 'order_status' in columns:
        # Find the count column (could be 'count', 'qty', 'total', 'status_count', etc.)
        count_col = None
        for col in columns:
            if any(keyword in col.lower() for keyword in ['count', 'qty', 'total']):
                count_col = col
                break
        
        if count_col:
            total_orders = sum(_as_int(row.get(count_col, 0)) for row in rows)
            most_common = max(rows, key=lambda r: _as_int(r.get(count_col, 0)))
            status = most_common.get('order_status', 'N/A')
            count = _as_int(most_common.get(count_col, 0))
            return f"Dos {_fmt_int_ptbr(total_orders)} pedidos, o status mais comum é '{status}' com {_fmt_int_ptbr(count)} pedidos."
    
    # Detect count queries
    if 'count(' in sql_lower or any(col.lower() in ['count', 'qty', 'total_orders'] for col in columns):
        if len(rows) == 1:
            count_val = _as_int(list(first_row.values())[0])
            if 'order' in sql_lower:
                return f"Existem {_fmt_int_ptbr(count_val)} pedidos no total."
            elif 'customer' in sql_lower:
                return f"Existem {_fmt_int_ptbr(count_val)} clientes únicos."
            elif 'product' in sql_lower:
                return f"Existem {_fmt_int_ptbr(count_val)} produtos no catálogo."
            else:
                return f"O total é {_fmt_int_ptbr(count_val)}."
    
    # Detect top-N queries
    if 'limit' in sql_lower and any(keyword in sql_lower for keyword in ['order by', 'desc']):
        if 'product_id' in columns:
            top_product = rows[0].get('product_id', 'N/A')
            sales = _as_float(rows[0].get('total_sales', 0))
            return f"O produto mais vendido é {top_product} com R$ {_fmt_float_ptbr(sales)} em vendas. Mostrando os {len(rows)} principais produtos."
    
    # Detect time series
    if 'period' in columns:
        total = sum(_as_int(row.get('qty', row.get('total_orders', 0))) for row in rows)
        periods = len(rows)
        return f"Análise temporal: {_fmt_int_ptbr(total)} pedidos distribuídos em {periods} períodos."
    
    # Detect distribution/grouping queries (customer_state, product_category, etc.)
    if any(col in columns for col in ['customer_state', 'product_category_name', 'seller_state']):
        # Find the count column
        count_col = None
        for col in columns:
            if any(keyword in col.lower() for keyword in ['count', 'qty', 'total']):
                count_col = col
                break
        
        if count_col and len(rows) > 1:
            total = sum(_as_int(row.get(count_col, 0)) for row in rows)
            
            # Show all results by default - no artificial limitations
            show_rows = rows
            suffix = f"Total: {len(rows)}"
            
            # Build response with user-friendly formatting
            if 'customer_state' in columns:
                # For states, use line-by-line format for better readability
                details = "\n".join([f"  {row['customer_state']}: {_fmt_int_ptbr(_as_int(row.get(count_col, 0)))}" for row in show_rows])
                return f"Distribuição de clientes por estado (total: {_fmt_int_ptbr(total)}):\n{details}\n\n{suffix} estados."
            elif 'product_category_name' in columns:
                # For categories, also use line-by-line for clarity
                details = "\n".join([f"  {row['product_category_name']}: {_fmt_int_ptbr(_as_int(row.get(count_col, 0)))}" for row in show_rows])
                return f"Distribuição por categoria (total: {_fmt_int_ptbr(total)}):\n{details}\n\n{suffix} categorias."
            elif 'seller_state' in columns:
                # For seller states, line-by-line format
                details = "\n".join([f"  {row['seller_state']}: {_fmt_int_ptbr(_as_int(row.get(count_col, 0)))}" for row in show_rows])
                return f"Distribuição de vendedores por estado (total: {_fmt_int_ptbr(total)}):\n{details}\n\n{suffix} estados."
    
    # Fallback to original functions based on shape
    if shape == "count":
        return _render_count_ptbr(rows, table)
    elif shape == "timeseries":
        return _render_timeseries_ptbr(rows, table, scale)
    else:
        return _render_preview_ptbr(rows, table, row_count, limit_applied)


def _render_count_ptbr(rows: list[Mapping[str, Any]], table: str | None) -> str:
    if not rows:
        return "Não foram encontrados dados para sua consulta."
    
    # Get the actual count value
    first_row = rows[0]
    
    # Try different possible column names for counts
    qty = 0
    count_col = None
    for col_name, value in first_row.items():
        if any(keyword in col_name.lower() for keyword in ['count', 'qty', 'total', 'quantidade']):
            qty = _as_int(value)
            count_col = col_name
            break
    
    if qty == 0 and len(first_row) == 1:
        # Fallback: use the first (and likely only) column
        qty = _as_int(list(first_row.values())[0])
        count_col = list(first_row.keys())[0]
    
    qfmt = _fmt_int_ptbr(qty)
    
    # Determine what we're counting based on table name and column name
    if table and 'order' in table.lower():
        if qty == 1:
            return f"Existe {qfmt} pedido no sistema."
        else:
            return f"Existem {qfmt} pedidos no sistema."
    elif table and 'customer' in table.lower():
        if qty == 1:
            return f"Existe {qfmt} cliente cadastrado."
        else:
            return f"Existem {qfmt} clientes cadastrados."
    elif table and 'product' in table.lower():
        if qty == 1:
            return f"Existe {qfmt} produto no catálogo."
        else:
            return f"Existem {qfmt} produtos no catálogo."
    else:
        # Generic fallback
        return f"O resultado da consulta é {qfmt}."


def _render_timeseries_ptbr(
    rows: list[Mapping[str, Any]], table: str | None, scale: str | None
) -> str:
    if not rows:
        alvo = f" na tabela `{table}`" if table else ""
        return f"Não encontrei dados de série temporal{alvo}."
    total = sum(_as_int(r.get("qty", 0)) for r in rows)
    qfmt = _fmt_int_ptbr(total)
    nper = len(rows)
    escala = {"month": "mensal", "week": "semanal", "day": "diária", "year": "anual"}.get(
        scale or "", "temporal"
    )
    alvo = f" na tabela `{table}`" if table else ""
    # Last 3 points, if available
    tail = rows[-3:]
    tail_str = ", ".join(
        f"{_fmt_period_ptbr(r.get('period'))}: {_fmt_int_ptbr(_as_int(r.get('qty', 0)))}"
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
        return "Não foram encontrados dados para sua consulta."
    
    shown = len(rows)
    first_row = rows[0]
    
    # Try to understand what kind of data this is
    columns = list(first_row.keys())
    
    # Check if this looks like an aggregation result
    if any(col.lower() in ['revenue', 'receita', 'total_sales', 'total_revenue'] for col in columns):
        # This is revenue/sales data
        if 'customer_state' in columns or 'state' in columns:
            return f"Aqui está a receita por estado. Mostrando os {shown} resultados:"
        elif 'product_id' in columns:
            return f"Aqui estão os produtos por receita. Mostrando os {shown} resultados:"
        else:
            return f"Aqui estão os resultados de receita. Mostrando {shown} registros:"
    
    elif any(col.lower() in ['count', 'qty', 'quantidade', 'total'] for col in columns):
        # This is count/quantity data
        if 'order_status' in columns:
            return f"Aqui está a distribuição por status dos pedidos. Mostrando {shown} categorias:"
        elif 'period' in columns:
            return f"Aqui está a evolução ao longo do tempo. Mostrando {shown} períodos:"
        else:
            return f"Aqui estão os totais por categoria. Mostrando {shown} resultados:"
    
    elif table and 'order' in table.lower():
        if limit_applied:
            return f"Aqui estão alguns pedidos encontrados (limitado a {shown} por segurança):"
        else:
            return f"Aqui estão os {shown} pedidos encontrados:"
    
    elif table and 'customer' in table.lower():
        if limit_applied:
            return f"Aqui estão alguns clientes encontrados (limitado a {shown} por segurança):"
        else:
            return f"Aqui estão os {shown} clientes encontrados:"
    
    else:
        # Generic fallback
        if limit_applied:
            return f"Aqui estão os resultados encontrados (limitado a {shown} por segurança):"
        else:
            return f"Aqui estão os {shown} resultados encontrados:"


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
    # Supports: FROM table, FROM schema.table, FROM "Schema"."Table", FROM table AS t
    m = re.search(
        r"""
        \bFROM\s+                              # FROM clause
        (?:                                     # first identifier (schema or table)
            "([^"]+)"                           # quoted part 1
            |                                   # or
            ([a-zA-Z_][\w$]*)                   # unquoted part 1
        )
        (?:                                     # optional .second identifier (table)
            \.
            (?:
                "([^"]+)"                       # quoted part 2
                |
                ([a-zA-Z_][\w$]*)               # unquoted part 2
            )
        )?
        """,
        sql,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    if not m:
        return None
    parts = [g for g in m.groups() if g]
    # Return last identifier (table name)
    return parts[-1]


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


def _as_int(x: Any) -> int:
    try:
        return int(round(float(x)))
    except Exception:
        return 0


def _as_float(x: Any) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


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
    if shape == "distribution":
        return [
            "Quer ver apenas os top 5?",
            "Deseja filtrar por período específico?",
            "Que tal cruzar com dados de vendas?",
        ]
    # preview
    base = f"{table} " if table else ""
    return [
        f"Adicionar filtros (ex.: data, status) em {base}?",
        f"Agregarmos por mês ou por vendedor em {base}?",
    ]
