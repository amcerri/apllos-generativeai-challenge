"""
Commerce document summarizer (PT‑BR humanized overview with risks/insights).

Overview
--------
Produce a concise Portuguese (pt-BR) summary from a normalized commerce
document (`CommerceDoc`). The summary highlights the document identity (type,
ID, currency), totals, key dates, and top items by value, and enumerates risks
reported by the extractor. The output follows the `Answer` contract when
available; otherwise a dict with equivalent fields is returned.

Design
------
- Input: a fully-populated `CommerceDoc` (from the extractor) or a mapping with
  the same structure.
- Output: Answer-like payload with: `text` (pt-BR), optional `artifacts` with
  the normalized document, and `meta` diagnostics (counts, totals, currency).
- No external I/O; dependency-light; logger/tracing are optional fallbacks.

Integration
-----------
- Called by the commerce agent after `detector` and `extractor`, before the
  final agent response.

Usage
-----
>>> from app.agents.commerce.summarizer import CommerceSummarizer
>>> from app.agents.commerce.extractor import CommerceDoc, CommerceDocHeader, CommerceTotals
>>> sm = CommerceSummarizer()
>>> # doc = CommerceDoc(...)
>>> # ans = sm.summarize(doc)
>>> # isinstance(ans, dict) or hasattr(ans, "text")
True
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final, Protocol, runtime_checkable

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:  # Optional config
    from app.config import get_config
except Exception:  # pragma: no cover - optional
    def get_config():
        return None


# Tracing (optional; single alias)
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


# A structural protocol to avoid hard coupling on the extractor's dataclass
@runtime_checkable
class CommerceDocLike(Protocol):
    doc: Any
    dates: Mapping[str, Any] | Any
    items: Sequence[Any]
    totals: Any
    risks: Sequence[str]


__all__ = ["CommerceSummarizer"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
class CommerceSummarizer:
    """Compose a PT‑BR summary from a normalized commerce document."""

    def __init__(self) -> None:
        self.log = get_logger("agent.commerce.summarizer")
        self._config = get_config()
        
        # Get configuration values with fallbacks
        if self._config is None:
            self.top_items = 3
            self.top_items_display = 10
            self.max_items_display = 5
        else:
            summarizer_config = self._config.get_commerce_summarizer_config()
            self.top_items = summarizer_config.get("top_items", 3)
            self.top_items_display = summarizer_config.get("top_items_display", 10)
            self.max_items_display = summarizer_config.get("max_items_display", 5)

    def summarize(self, doc: CommerceDocLike | Mapping[str, Any]) -> Any:
        """
        Return an Answer-like payload with a business-friendly summary.

        Args:
            doc: `CommerceDoc` or mapping with the same structure.

        Returns:
            Answer-like payload with text, meta, and artifacts.

        Raises:
            ValueError: If document structure is invalid.
            RuntimeError: If summarization fails.
        """
        with start_span("agent.commerce.summarize"):
            dv = _DocView.from_obj(doc)
            text = _render_ptbr(dv, top_k=self.top_items, top_items_display=self.top_items_display, max_items_display=self.max_items_display)

            meta = {
                "doc_type": dv.doc_type,
                "doc_id": dv.doc_id,
                "currency": dv.currency,
                "item_count": len(dv.items),
                "grand_total": dv.totals.get("grand_total"),
                "risks_count": len(dv.risks),
            }

            payload = {
                "text": text,
                "meta": meta,
                "artifacts": {"normalized_doc": dv.to_dict()},
                "followups": _suggest_followups(dv),
            }
            return _coerce_answer(payload)


# ---------------------------------------------------------------------------
# Internal normalized view (stable access regardless of concrete type)
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class _Item:
    line_no: int | None
    name: str | None
    qty: float | None
    unit_price: float | None
    line_total: float | None


@dataclass(slots=True)
class _DocView:
    doc_type: str | None
    doc_id: str | None
    currency: str | None
    issue_date: str | None
    due_date: str | None
    items: list[_Item]
    totals: dict[str, Any]
    risks: list[str]

    @classmethod
    def from_obj(cls, obj: CommerceDocLike | Mapping[str, Any]) -> _DocView:
        if isinstance(obj, Mapping):
            doc = obj.get("doc", {})
            dates = obj.get("dates", {})
            items_raw = obj.get("items", []) or []
            totals = obj.get("totals", {}) or {}
            # Build view
            items: list[_Item] = []
            for it in items_raw:
                if isinstance(it, Mapping):
                    items.append(
                        _Item(
                            line_no=_as_int(it.get("line_no")),
                            name=_as_str(it.get("name")),
                            qty=_as_float(it.get("qty")),
                            unit_price=_as_float(it.get("unit_price")),
                            line_total=_as_float(it.get("line_total")),
                        )
                    )
            return cls(
                doc_type=_as_str((doc or {}).get("doc_type")),
                doc_id=_as_str((doc or {}).get("doc_id")),
                currency=_as_str((doc or {}).get("currency")),
                issue_date=_as_str((dates or {}).get("issue_date")),
                due_date=_as_str((dates or {}).get("due_date")),
                items=items,
                totals=dict(totals),
                risks=list(obj.get("risks", []) or []),
            )
        # Access via attributes (dataclass from extractor)
        ddoc = getattr(obj, "doc", None)
        dates = getattr(obj, "dates", {})
        items_raw = list(getattr(obj, "items", []) or [])
        totals_obj = getattr(obj, "totals", None)
        to_dict_fn = getattr(totals_obj, "to_dict", None)
        if callable(to_dict_fn):
            totals = to_dict_fn()
        else:
            totals = dict(totals_obj or {})
        items2: list[_Item] = []
        for it in items_raw:
            items2.append(
                _Item(
                    line_no=getattr(it, "line_no", None),
                    name=getattr(it, "name", None),
                    qty=getattr(it, "qty", None),
                    unit_price=getattr(it, "unit_price", None),
                    line_total=getattr(it, "line_total", None),
                )
            )
        return cls(
            doc_type=getattr(ddoc, "doc_type", None),
            doc_id=getattr(ddoc, "doc_id", None),
            currency=getattr(ddoc, "currency", None),
            issue_date=str((dates or {}).get("issue_date")) if isinstance(dates, Mapping) else None,
            due_date=str((dates or {}).get("due_date")) if isinstance(dates, Mapping) else None,
            items=items2,
            totals=totals,
            risks=list(getattr(obj, "risks", []) or []),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc": {
                "doc_type": self.doc_type,
                "doc_id": self.doc_id,
                "currency": self.currency,
            },
            "dates": {"issue_date": self.issue_date, "due_date": self.due_date},
            "items": [
                {
                    "line_no": it.line_no,
                    "name": it.name,
                    "qty": it.qty,
                    "unit_price": it.unit_price,
                    "line_total": it.line_total,
                }
                for it in self.items
            ],
            "totals": dict(self.totals),
            "risks": list(self.risks),
        }


# ---------------------------------------------------------------------------
# Rendering helpers (pt-BR)
# ---------------------------------------------------------------------------


def _render_ptbr(doc: _DocView, *, top_k: int, top_items_display: int = 10, max_items_display: int = 5) -> str:
    tipo = _label_doc_type(doc.doc_type)
    moeda = doc.currency or "(não informada)"
    simbolo = _currency_symbol(moeda)
    total_txt = _fmt_money(doc.totals.get("grand_total"), simbolo)

    linhas = []

    # === CABEÇALHO ===
    linhas.append("INFORMAÇÕES DO DOCUMENTO")
    linhas.append("=" * 50)
    linhas.append(f"Tipo: {tipo}")
    linhas.append(f"ID: {doc.doc_id or '(sem ID)'}")
    linhas.append(f"Moeda: {moeda}")
    linhas.append("")

    # === DATAS ===
    if doc.issue_date or doc.due_date:
        linhas.append("DATAS")
        linhas.append("-" * 30)
        if doc.issue_date:
            linhas.append(f"Emissão: {doc.issue_date}")
        if doc.due_date:
            linhas.append(f"Vencimento: {doc.due_date}")
        linhas.append("")

    # === TOTAIS ===
    linhas.append("VALORES TOTAIS")
    linhas.append("-" * 30)
    sub = _fmt_money(doc.totals.get("subtotal"), simbolo)
    frete = _fmt_money(doc.totals.get("freight"), simbolo)
    linhas.append(f"Subtotal: {sub}")
    linhas.append(f"Frete: {frete}")
    linhas.append(f"TOTAL GERAL: {total_txt}")
    linhas.append("")

    # === ITENS PRINCIPAIS ===
    itens_ordenados = sorted(
        doc.items,
        key=lambda it: (it.line_total or 0.0),
        reverse=True,
    )
    if itens_ordenados:
        linhas.append("ITENS PRINCIPAIS")
        linhas.append("-" * 30)
        
        # Para poucos itens (até top_items_display), mostrar todos. Para muitos, usar max_items_display
        total_itens = len(itens_ordenados)
        if total_itens <= top_items_display:
            # Mostrar todos os itens
            for i, it in enumerate(itens_ordenados, 1):
                qtd = _fmt_float_ptbr(it.qty) if it.qty is not None else "?"
                up = _fmt_money(it.unit_price, simbolo)
                lt = _fmt_money(it.line_total, simbolo)
                nome = it.name or "(sem descrição)"
                linhas.append(f"{i}. {nome}")
                linhas.append(f"   Quantidade: {qtd}")
                linhas.append(f"   Preço unitário: {up}")
                linhas.append(f"   Total da linha: {lt}")
                linhas.append("")
        else:
            # Para muitos itens, usar max_items_display e mostrar resumo
            for i, it in enumerate(itens_ordenados[: max(1, int(max_items_display))], 1):
                qtd = _fmt_float_ptbr(it.qty) if it.qty is not None else "?"
                up = _fmt_money(it.unit_price, simbolo)
                lt = _fmt_money(it.line_total, simbolo)
                nome = it.name or "(sem descrição)"
                linhas.append(f"{i}. {nome}")
                linhas.append(f"   Quantidade: {qtd}")
                linhas.append(f"   Preço unitário: {up}")
                linhas.append(f"   Total da linha: {lt}")
                linhas.append("")
            
            # Mostrar total de itens se houver mais que os mostrados
            if total_itens > max_items_display:
                linhas.append(f"... e mais {total_itens - max_items_display} itens")
                linhas.append("")

    # === RISCOS E ALERTAS ===
    if doc.risks:
        linhas.append("RISCOS E ALERTAS")
        linhas.append("-" * 30)
        for r in doc.risks[:10]:
            # Verificar se é um erro de LLM
            if r.startswith("llm_error:"):
                error_type = r.replace("llm_error:", "")
                linhas.append(f"- Erro de processamento ({error_type}): Falha na análise automática do documento")
            else:
                # Explicar cada risco de forma clara
                explicacao = _explicar_risco(r)
                linhas.append(f"- {r}: {explicacao}")
        linhas.append("")

    # === INTERAÇÃO ===
    linhas.append("INTERAÇÃO")
    linhas.append("-" * 30)
    if total_txt != "(não informado)":
        linhas.append("Gostaria de alguma análise específica sobre este pedido?")
        linhas.append("Posso ajudar com comparações, simulações ou análises detalhadas.")
    else:
        linhas.append("Este documento apresenta algumas inconsistências nos valores.")
        linhas.append("Posso ajudar a investigar ou analisar os dados disponíveis.")

    return "\n".join(linhas)


def _explicar_risco(risco: str) -> str:
    """Explica o significado de cada tipo de risco de forma clara."""
    explicacoes = {
        "sum_mismatch": "A soma dos itens não confere com o subtotal declarado",
        "grand_total_mismatch": "O total geral não confere com subtotal + frete",
        "missing_core_fields": "Campos essenciais como ID, data ou valores estão ausentes",
        "incomplete_lines": "Alguns itens não possuem informações completas",
        "currency_mismatch": "Há inconsistências na moeda utilizada",
        "date_inconsistency": "As datas apresentam inconsistências ou estão ausentes",
        "price_anomaly": "Preços muito altos ou baixos que podem indicar erro",
        "quantity_anomaly": "Quantidades muito altas ou baixas que podem indicar erro",
        "duplicate_items": "Itens duplicados encontrados no pedido",
        "tax_calculation_error": "Erro no cálculo de impostos ou taxas",
        "shipping_cost_anomaly": "Custo de frete muito alto ou baixo",
        "vendor_mismatch": "Inconsistências nos dados do fornecedor",
        "payment_terms_missing": "Condições de pagamento não especificadas",
        "delivery_address_missing": "Endereço de entrega não informado",
        "contact_info_missing": "Informações de contato ausentes",
    }
    return explicacoes.get(risco, "Risco não identificado - requer análise manual")


def _label_doc_type(t: str | None) -> str:
    if not t:
        return "(tipo não identificado)"
    labels = {
        "invoice": "Fatura (Invoice)",
        "purchase_order": "Pedido de Compra (PO)",
        "order_form": "Order Form",
        "beo": "Banquet Event Order (BEO)",
        "receipt": "Recibo",
        "quote": "Cotação/Proposta",
    }
    return labels.get(t, t)


def _currency_symbol(code: str) -> str:
    c = (code or "").upper()
    return {
        "BRL": "R$",
        "USD": "US$",
        "EUR": "€",
        "GBP": "£",
        "ARS": "$",
        "CLP": "$",
        "MXN": "$",
    }.get(c, c or "$")


def _fmt_money(v: Any, sym: str) -> str:
    if v is None:
        return "(não informado)"
    try:
        f = float(v)
    except Exception:
        return "(não informado)"
    return f"{sym} {f:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _fmt_float_ptbr(v: float | None) -> str:
    if v is None:
        return "(não informado)"
    return f"{v:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _as_str(v: Any) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _as_int(v: Any) -> int | None:
    try:
        return int(str(v).strip())
    except Exception:
        return None


def _as_float(v: Any) -> float | None:
    try:
        return float(v)
    except Exception:
        return None


def _suggest_followups(doc: _DocView) -> list[str]:
    base = "este documento"
    outs: list[str] = []
    if doc.items:
        outs.append(f"Quer que eu exporte os itens de {base} em CSV?")
    if doc.doc_type == "invoice":
        outs.append("Deseja que eu valide impostos e descontos informados?")
    if doc.doc_type == "purchase_order":
        outs.append("Posso cruzar com recebimentos para ver divergências.")
    if not outs:
        outs.append(
            "Posso detalhar mais campos (datas, condições) ou comparar com outros documentos."
        )
    return outs


# ---------------------------------------------------------------------------
# Answer coercion
# ---------------------------------------------------------------------------


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
