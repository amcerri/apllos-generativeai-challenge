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
    from app.config.settings import get_settings as get_config
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
        
        # Get configuration values with fallbacks using Settings model
        try:
            summarizer_cfg = getattr(getattr(self._config, "commerce"), "summarizer")  # type: ignore[attr-defined]
            self.top_items = int(getattr(summarizer_cfg, "top_items", 3))
            self.top_items_display = int(getattr(summarizer_cfg, "top_items_display", 10))
            self.max_items_display = int(getattr(summarizer_cfg, "max_items_display", 5))
        except Exception:
            self.top_items = 3
            self.top_items_display = 10
            self.max_items_display = 5

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
            language = _detect_language(dv)
            text = _render_multilang(dv, language=language, top_k=self.top_items, top_items_display=self.top_items_display, max_items_display=self.max_items_display)

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
    buyer: dict[str, Any]
    vendor: dict[str, Any]
    shipping: dict[str, Any]
    terms: dict[str, Any]
    dates_full: dict[str, Any]
    meta: dict[str, Any]

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
                buyer=dict(obj.get("buyer") or {}),
                vendor=dict(obj.get("vendor") or {}),
                shipping=dict(obj.get("shipping") or {}),
                terms=dict(obj.get("terms") or {}),
                dates_full=dict(dates or {}),
                meta=dict(obj.get("meta") or {}),
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
        buyer_obj = getattr(obj, "buyer", {})
        vendor_obj = getattr(obj, "vendor", {})
        shipping_obj = getattr(obj, "shipping", {})
        terms_obj = getattr(obj, "terms", None)
        meta_obj = getattr(obj, "meta", {})
        
        return cls(
            doc_type=getattr(ddoc, "doc_type", None),
            doc_id=getattr(ddoc, "doc_id", None),
            currency=getattr(ddoc, "currency", None),
            issue_date=str((dates or {}).get("issue_date")) if isinstance(dates, Mapping) else None,
            due_date=str((dates or {}).get("due_date")) if isinstance(dates, Mapping) else None,
            items=items2,
            totals=totals,
            risks=list(getattr(obj, "risks", []) or []),
            buyer=dict(buyer_obj) if isinstance(buyer_obj, Mapping) else {},
            vendor=dict(vendor_obj) if isinstance(vendor_obj, Mapping) else {},
            shipping=dict(shipping_obj) if isinstance(shipping_obj, Mapping) else {},
            terms=dict(terms_obj) if isinstance(terms_obj, Mapping) else {},
            dates_full=dict(dates) if isinstance(dates, Mapping) else {},
            meta=dict(meta_obj) if isinstance(meta_obj, Mapping) else {},
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
# Language detection and multilang rendering
# ---------------------------------------------------------------------------


def _has_value(value: Any) -> bool:
    """Check if a value is considered non-empty.
    
    Returns False for None, empty strings, empty lists, empty dicts, and 0.
    """
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return len(value) > 0
    if isinstance(value, (int, float)):
        return value != 0
    return True


def _dict_has_any_value(d: dict[str, Any] | None) -> bool:
    """Check if a dictionary has any non-empty values."""
    if not d:
        return False
    return any(_has_value(v) for v in d.values())


def _format_dict_readable(d: dict[str, Any], symbol: str = "", indent: int = 0) -> str:
    """Format a dictionary in a human-readable way.
    
    Parameters
    ----------
    d: Dictionary to format
    symbol: Currency symbol for formatting numbers
    indent: Indentation level for nested structures
    
    Returns
    -------
    Formatted string representation
    """
    if not d:
        return ""
    
    lines = []
    prefix = "  " * indent
    
    for key, value in sorted(d.items()):
        if not _has_value(value):
            continue
        
        # Format key name
        key_label = key.replace("_", " ").strip()
        key_label = " ".join(word.capitalize() if word else "" for word in key_label.split())
        
        # Format value based on type
        if isinstance(value, dict):
            # Nested dict - format recursively
            nested_str = _format_dict_readable(value, symbol, indent + 1)
            if nested_str:
                lines.append(f"{prefix}{key_label}:")
                lines.append(nested_str)
        elif isinstance(value, list):
            # List - format each item
            if value:
                lines.append(f"{prefix}{key_label}:")
                for item in value:
                    if isinstance(item, dict):
                        item_str = _format_dict_readable(item, symbol, indent + 1)
                        lines.append(item_str)
                    else:
                        formatted_item = _format_field_value(item, symbol)
                        if formatted_item:
                            lines.append(f"{prefix}  - {formatted_item}")
        else:
            # Simple value
            formatted_value = _format_field_value(value, symbol)
            if formatted_value:
                lines.append(f"{prefix}{key_label}: {formatted_value}")
    
    return "\n".join(lines)


def _format_field_value(value: Any, symbol: str = "") -> str:
    """Format a field value for display based on its type."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        if symbol:
            return f"{symbol} {value:,.2f}" if value != 0 else ""
        return f"{value:,.2f}"
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        # Format dict in readable way (single line for simple dicts, multi-line for complex)
        if len(value) <= 3 and all(isinstance(v, (str, int, float)) for v in value.values()):
            # Simple dict - format inline
            parts = []
            for k, v in sorted(value.items()):
                k_label = k.replace("_", " ").strip().capitalize()
                v_str = _format_field_value(v, symbol)
                if v_str:
                    parts.append(f"{k_label}: {v_str}")
            return ", ".join(parts) if parts else ""
        else:
            # Complex dict - will be handled by caller with _format_dict_readable
            return ""
    if isinstance(value, list):
        if len(value) == 0:
            return ""
        # Format list items
        formatted_items = []
        for item in value:
            if isinstance(item, dict):
                # Format dict items inline if simple
                if len(item) <= 3 and all(isinstance(v, (str, int, float)) for v in item.values()):
                    parts = []
                    for k, v in sorted(item.items()):
                        k_label = k.replace("_", " ").strip().capitalize()
                        v_str = _format_field_value(v, symbol)
                        if v_str:
                            parts.append(f"{k_label}: {v_str}")
                    formatted_items.append("; ".join(parts))
                else:
                    # Complex dict in list - format as readable text
                    parts = []
                    for k, v in sorted(item.items()):
                        if _has_value(v):
                            k_label = k.replace("_", " ").strip().capitalize()
                            v_str = _format_field_value(v, symbol)
                            if v_str:
                                parts.append(f"{k_label}: {v_str}")
                    formatted_items.append(", ".join(parts))
            else:
                formatted_item = _format_field_value(item, symbol)
                if formatted_item:
                    formatted_items.append(formatted_item)
        return "; ".join(formatted_items) if formatted_items else ""
    return str(value)


def _render_dict_section(d: dict[str, Any], title: str, language: str, symbol: str = "") -> list[str]:
    """Dynamically render a dictionary section showing only fields with values.
    
    Parameters
    ----------
    d: Dictionary to render
    title: Section title (empty string to skip title)
    language: 'pt' or 'en' for labels
    symbol: Currency symbol for formatting numbers
    
    Returns
    -------
    List of lines to add to the output
    """
    if not _dict_has_any_value(d):
        return []
    
    lines = []
    if title:
        lines.append(title)
        lines.append("-" * 50)
    
    # Display fields exactly as extracted - no keyword translation or fixed labels
    # Only format the display nicely (capitalize first letter, replace underscores)
    for key, value in sorted(d.items()):
        if not _has_value(value):
            continue
        
        # Skip internal/metadata fields
        if key.startswith("_") or key in ("source_filename", "source_mime", "extracted_at", "extraction_method"):
            continue
        
        # Format the label from the key name (just cosmetic, no translation)
        label = key.replace("_", " ").strip()
        label = " ".join(word.capitalize() if word else "" for word in label.split())
        
        # Format the value based on its type
        if isinstance(value, dict):
            # Complex dict - format with readable structure
            formatted_dict = _format_dict_readable(value, symbol, indent=0)
            if formatted_dict:
                lines.append(f"{label}:")
                # Indent each line of the formatted dict
                for line in formatted_dict.split("\n"):
                    if line.strip():
                        lines.append(f"  {line}")
        elif isinstance(value, list):
            # List - format items
            if value:
                lines.append(f"{label}:")
                for item in value:
                    if isinstance(item, dict):
                        # Format dict items in a readable way
                        item_parts = []
                        for k, v in sorted(item.items()):
                            if _has_value(v):
                                k_label = k.replace("_", " ").strip().capitalize()
                                v_str = _format_field_value(v, symbol)
                                if v_str:
                                    item_parts.append(f"{k_label}: {v_str}")
                        if item_parts:
                            lines.append(f"  - {', '.join(item_parts)}")
                    else:
                        formatted_item = _format_field_value(item, symbol)
                        if formatted_item:
                            lines.append(f"  - {formatted_item}")
        else:
            # Simple value
            formatted_value = _format_field_value(value, symbol)
            if formatted_value:
                lines.append(f"{label}: {formatted_value}")
    
    # Only add blank line if we have content (accounting for optional title)
    if len(lines) > (2 if title else 0):
        lines.append("")
        return lines
    
    return []


def _detect_language(doc: _DocView) -> str:
    """Detect document language based on document content, not just currency.
    
    Returns 'en' for English or 'pt' for Portuguese (defaults to 'pt').
    """
    # Priority 1: Check document metadata and fields for language indicators
    # Check vendor/buyer names and addresses for Portuguese indicators
    portuguese_indicators = []
    english_indicators = []
    
    # Check vendor fields
    if doc.vendor:
        vendor_text = " ".join([str(v).lower() for v in doc.vendor.values() if v])
        portuguese_indicators.extend([
            "ltda", "cnpj", "cpf", "brasil", "brasileiro", "são paulo", "rio de janeiro",
            "cep", "endereço", "telefone", "empresa", "fornecedor"
        ])
        english_indicators.extend([
            "inc", "llc", "corp", "ltd", "company", "street", "avenue", "road",
            "phone", "address", "zip code", "vendor", "supplier"
        ])
        pt_count = sum(1 for ind in portuguese_indicators if ind in vendor_text)
        en_count = sum(1 for ind in english_indicators if ind in vendor_text)
        if pt_count > en_count and pt_count > 0:
            return "pt"
        if en_count > pt_count and en_count > 0:
            return "en"
    
    # Check buyer fields
    if doc.buyer:
        buyer_text = " ".join([str(v).lower() for v in doc.buyer.values() if v])
        pt_count = sum(1 for ind in portuguese_indicators if ind in buyer_text)
        en_count = sum(1 for ind in english_indicators if ind in buyer_text)
        if pt_count > en_count and pt_count > 0:
            return "pt"
        if en_count > pt_count and en_count > 0:
            return "en"
    
    # Priority 2: Check item names and descriptions for language
    english_keywords = {"order", "item", "quantity", "price", "total", "subtotal", "shipping", "tax", "unit", "amount"}
    portuguese_keywords = {"pedido", "item", "quantidade", "preço", "total", "subtotal", "frete", "imposto", "unidade", "valor", "produto", "serviço"}
    
    item_text = " ".join([(it.name or "").lower() + " " + (it.description or "").lower() for it in doc.items[:10]])
    en_count = sum(1 for kw in english_keywords if kw in item_text)
    pt_count = sum(1 for kw in portuguese_keywords if kw in item_text)
    
    if pt_count > en_count and pt_count > 0:
        return "pt"
    if en_count > pt_count and en_count > 0:
        return "en"
    
    # Priority 3: Currency is a weak indicator (documents can be in Portuguese with USD)
    # Only use currency if we have no other indicators
    currency = (doc.currency or "").upper()
    if currency == "BRL" or currency in {"ARS", "CLP", "MXN"}:
        return "pt"
    if currency in {"USD", "GBP", "EUR", "CAD", "AUD", "NZD"} and not item_text.strip():
        # Only use currency as indicator if we have no item text to analyze
        return "en"
    
    # Default to Portuguese (pt-BR is the primary language for this system)
    return "pt"


def _render_multilang(doc: _DocView, *, language: str = "pt", top_k: int, top_items_display: int = 10, max_items_display: int = 5) -> str:
    """Render document summary in the specified language."""
    if language == "en":
        return _render_en(doc, top_k=top_k, top_items_display=top_items_display, max_items_display=max_items_display)
    else:
        return _render_ptbr(doc, top_k=top_k, top_items_display=top_items_display, max_items_display=max_items_display)


def _render_ptbr(doc: _DocView, *, top_k: int, top_items_display: int = 10, max_items_display: int = 5) -> str:
    tipo = _label_doc_type(doc.doc_type)
    moeda = doc.currency or ""
    simbolo = _currency_symbol(moeda) if moeda else ""
    total_txt = _fmt_money(doc.totals.get("grand_total"), simbolo)

    linhas = []

    # === CABEÇALHO ===
    linhas.append("INFORMAÇÕES DO DOCUMENTO")
    linhas.append("=" * 50)
    linhas.append(f"Tipo: {tipo}")
    if _has_value(doc.doc_id):
        linhas.append(f"ID: {doc.doc_id}")
    if _has_value(doc.currency):
        linhas.append(f"Moeda: {doc.currency}")
    linhas.append("")
    
    # === VENDOR/BUYER (dynamic sections) ===
    # Show vendor/buyer sections only if they have data
    if _dict_has_any_value(doc.vendor):
        vendor_lines = _render_dict_section(doc.vendor, "", "pt", simbolo)
        linhas.extend(vendor_lines)
    
    if _dict_has_any_value(doc.buyer):
        buyer_lines = _render_dict_section(doc.buyer, "", "pt", simbolo)
        linhas.extend(buyer_lines)

    # === DATAS ===
    if _dict_has_any_value(doc.dates_full):
        linhas.append("DATAS")
        linhas.append("-" * 50)
        for key, value in sorted(doc.dates_full.items()):
            if not _has_value(value):
                continue
            # Skip internal/metadata fields
            if key.startswith("_") or key in ("source_filename", "source_mime", "extracted_at", "extraction_method"):
                continue
            # Format the label
            label = key.replace("_", " ").strip()
            label = " ".join(word.capitalize() if word else "" for word in label.split())
            linhas.append(f"{label}: {value}")
        linhas.append("")

    # === TOTAIS ===
    if _dict_has_any_value(doc.totals):
        linhas.append("VALORES TOTAIS")
        linhas.append("-" * 50)
        totals_dict = dict(doc.totals)
        
        # Show grand_total first if available
        if "grand_total" in totals_dict and _has_value(totals_dict["grand_total"]):
            linhas.append(f"TOTAL GERAL: {total_txt}")
        
        # Then show other totals (subtotal, freight, taxes, etc.)
        for key, value in sorted(totals_dict.items()):
            if key == "grand_total":
                continue  # Already shown above
            if not _has_value(value):
                continue
            
            # Format the label
            label = key.replace("_", " ").strip()
            label = " ".join(word.capitalize() if word else "" for word in label.split())
            
            # Format money values
            if isinstance(value, (int, float)):
                formatted_value = _fmt_money(value, simbolo)
            elif isinstance(value, list):
                # Handle arrays (taxes, discounts, etc.) - format readably
                if value:
                    linhas.append(f"{label}:")
                    for item in value:
                        if isinstance(item, dict):
                            # Format dict items in a readable way
                            item_parts = []
                            for k, v in sorted(item.items()):
                                if _has_value(v):
                                    k_label = k.replace("_", " ").strip().capitalize()
                                    if isinstance(v, (int, float)):
                                        v_str = _fmt_money(v, simbolo)
                                    else:
                                        v_str = str(v)
                                    if v_str:
                                        item_parts.append(f"{k_label}: {v_str}")
                            if item_parts:
                                linhas.append(f"  - {', '.join(item_parts)}")
                        else:
                            item_str = _format_field_value(item, simbolo)
                            if item_str:
                                linhas.append(f"  - {item_str}")
                    continue  # Skip the normal append since we already added lines
                else:
                    formatted_value = ""
            else:
                formatted_value = _format_field_value(value, simbolo)
            
            if formatted_value:
                linhas.append(f"{label}: {formatted_value}")
        linhas.append("")

    # === ITENS PRINCIPAIS ===
    itens_ordenados = sorted(
        doc.items,
        key=lambda it: (it.line_total or 0.0),
        reverse=True,
    )
    if itens_ordenados:
        linhas.append("ITENS PRINCIPAIS")
        linhas.append("-" * 50)
        
        # Mostrar TODOS os itens - sem limite para commerce agent
        for i, it in enumerate(itens_ordenados, 1):
            qtd = _fmt_float_ptbr(it.qty) if it.qty is not None else "?"
            up = _fmt_money(it.unit_price, simbolo) if it.unit_price is not None else "(não informado)"
            lt = _fmt_money(it.line_total, simbolo) if it.line_total is not None else "(não informado)"
            nome = it.name or "(sem descrição)"
            
            # Format item with proper spacing and line breaks
            linhas.append(f"{i}. {nome}")
            linhas.append(f"   Quantidade: {qtd}")
            linhas.append(f"   Preço unitário: {up}")
            linhas.append(f"   Total da linha: {lt}")
            linhas.append("")

    # === RISCOS E ALERTAS ===
    if doc.risks:
        linhas.append("RISCOS E ALERTAS")
        linhas.append("-" * 50)
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
    linhas.append("-" * 50)
    if total_txt != "(não informado)":
        linhas.append("Gostaria de alguma análise específica sobre este pedido?")
        linhas.append("Posso ajudar com comparações, simulações ou análises detalhadas.")
    else:
        linhas.append("Este documento apresenta algumas inconsistências nos valores.")
        linhas.append("Posso ajudar a investigar ou analisar os dados disponíveis.")

    return "\n".join(linhas)


def _render_en(doc: _DocView, *, top_k: int, top_items_display: int = 10, max_items_display: int = 5) -> str:
    """Render document summary in English."""
    tipo = _label_doc_type_en(doc.doc_type)
    currency = doc.currency or ""
    symbol = _currency_symbol(currency) if currency else ""
    total_txt = _fmt_money_en(doc.totals.get("grand_total"), symbol)

    lines = []

    # === HEADER ===
    lines.append("DOCUMENT INFORMATION")
    lines.append("=" * 50)
    lines.append(f"Type: {tipo}")
    if _has_value(doc.doc_id):
        lines.append(f"ID: {doc.doc_id}")
    if _has_value(doc.currency):
        lines.append(f"Currency: {doc.currency}")
    lines.append("")
    
    # === VENDOR/BUYER (dynamic sections) ===
    # Show vendor/buyer sections only if they have data
    if _dict_has_any_value(doc.vendor):
        vendor_lines = _render_dict_section(doc.vendor, "", "en", symbol)
        lines.extend(vendor_lines)
    
    if _dict_has_any_value(doc.buyer):
        buyer_lines = _render_dict_section(doc.buyer, "", "en", symbol)
        lines.extend(buyer_lines)

    # === DATES ===
    if _dict_has_any_value(doc.dates_full):
        lines.append("DATES")
        lines.append("-" * 50)
        for key, value in sorted(doc.dates_full.items()):
            if not _has_value(value):
                continue
            # Skip internal/metadata fields
            if key.startswith("_") or key in ("source_filename", "source_mime", "extracted_at", "extraction_method"):
                continue
            # Format the label
            label = key.replace("_", " ").strip()
            label = " ".join(word.capitalize() if word else "" for word in label.split())
            lines.append(f"{label}: {value}")
        lines.append("")

    # === TOTALS ===
    if _dict_has_any_value(doc.totals):
        lines.append("TOTAL VALUES")
        lines.append("-" * 50)
        totals_dict = dict(doc.totals)
        
        # Show grand_total first if available
        if "grand_total" in totals_dict and _has_value(totals_dict["grand_total"]):
            lines.append(f"GRAND TOTAL: {total_txt}")
        
        # Then show other totals (subtotal, freight, taxes, etc.)
        for key, value in sorted(totals_dict.items()):
            if key == "grand_total":
                continue  # Already shown above
            if not _has_value(value):
                continue
            
            # Format the label
            label = key.replace("_", " ").strip()
            label = " ".join(word.capitalize() if word else "" for word in label.split())
            
            # Format money values
            if isinstance(value, (int, float)):
                formatted_value = _fmt_money_en(value, symbol)
            elif isinstance(value, list):
                # Handle arrays (taxes, discounts, etc.) - format readably
                if value:
                    lines.append(f"{label}:")
                    for item in value:
                        if isinstance(item, dict):
                            # Format dict items in a readable way
                            item_parts = []
                            for k, v in sorted(item.items()):
                                if _has_value(v):
                                    k_label = k.replace("_", " ").strip().capitalize()
                                    if isinstance(v, (int, float)):
                                        v_str = _fmt_money_en(v, symbol)
                                    else:
                                        v_str = str(v)
                                    if v_str:
                                        item_parts.append(f"{k_label}: {v_str}")
                            if item_parts:
                                lines.append(f"  - {', '.join(item_parts)}")
                        else:
                            item_str = _format_field_value(item, symbol)
                            if item_str:
                                lines.append(f"  - {item_str}")
                    continue  # Skip the normal append since we already added lines
                else:
                    formatted_value = ""
            else:
                formatted_value = _format_field_value(value, symbol)
            
            if formatted_value:
                lines.append(f"{label}: {formatted_value}")
        lines.append("")

    # === TOP ITEMS ===
    sorted_items = sorted(
        doc.items,
        key=lambda it: (it.line_total or 0.0),
        reverse=True,
    )
    if sorted_items:
        lines.append("TOP ITEMS")
        lines.append("-" * 50)
        
        # Show ALL items - no limit for commerce agent
        for i, it in enumerate(sorted_items, 1):
            qty = _fmt_float_en(it.qty) if it.qty is not None else "?"
            up = _fmt_money_en(it.unit_price, symbol) if it.unit_price is not None else "(not specified)"
            lt = _fmt_money_en(it.line_total, symbol) if it.line_total is not None else "(not specified)"
            name = it.name or "(no description)"
            
            # Format item with proper spacing and line breaks
            lines.append(f"{i}. {name}")
            lines.append(f"   Quantity: {qty}")
            lines.append(f"   Unit Price: {up}")
            lines.append(f"   Line Total: {lt}")
            lines.append("")

    # === RISKS AND ALERTS ===
    if doc.risks:
        lines.append("RISKS AND ALERTS")
        lines.append("-" * 50)
        for r in doc.risks[:10]:
            # Check if it's an LLM error
            if r.startswith("llm_error:"):
                error_type = r.replace("llm_error:", "")
                lines.append(f"- Processing Error ({error_type}): Failed to automatically analyze document")
            else:
                # Explain each risk clearly
                explanation = _explain_risk_en(r)
                lines.append(f"- {r}: {explanation}")
        lines.append("")

    # === INTERACTION ===
    lines.append("INTERACTION")
    lines.append("-" * 50)
    if total_txt != "(not specified)":
        lines.append("Would you like any specific analysis on this order?")
        lines.append("I can help with comparisons, simulations, or detailed analyses.")
    else:
        lines.append("This document presents some inconsistencies in the values.")
        lines.append("I can help investigate or analyze the available data.")

    return "\n".join(lines)


def _explain_risk_en(risk: str) -> str:
    """Explain the meaning of each risk type clearly in English."""
    explanations = {
        "sum_mismatch": "Item sum does not match declared subtotal",
        "grand_total_mismatch": "Grand total does not match subtotal + shipping",
        "missing_core_fields": "Essential fields such as ID, date, or values are missing",
        "incomplete_lines": "Some items lack complete information",
        "currency_mismatch": "Inconsistencies in the currency used",
        "date_inconsistency": "Dates present inconsistencies or are missing",
        "price_anomaly": "Very high or low prices that may indicate an error",
        "quantity_anomaly": "Very high or low quantities that may indicate an error",
        "duplicate_items": "Duplicate items found in the order",
        "tax_calculation_error": "Error in tax or fee calculation",
        "shipping_cost_anomaly": "Shipping cost is very high or low",
        "vendor_mismatch": "Inconsistencies in vendor data",
        "payment_terms_missing": "Payment terms not specified",
        "delivery_address_missing": "Delivery address not provided",
        "contact_info_missing": "Contact information missing",
    }
    return explanations.get(risk, "Unidentified risk - requires manual analysis")


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


def _label_doc_type_en(t: str | None) -> str:
    if not t:
        return "(type not identified)"
    labels = {
        "invoice": "Invoice",
        "purchase_order": "Purchase Order (PO)",
        "order_form": "Order Form",
        "beo": "Banquet Event Order (BEO)",
        "receipt": "Receipt",
        "quote": "Quote/Proposal",
        "contract": "Contract",
        "shipping_notice": "Shipping Notice",
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
    # Format with proper spacing: R$ 9.360,40
    formatted = f"{f:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{sym} {formatted}" if sym else formatted


def _fmt_money_en(v: Any, sym: str) -> str:
    if v is None:
        return "(not specified)"
    try:
        f = float(v)
    except Exception:
        return "(not specified)"
    # Format with proper spacing: US$ 9,360.40
    formatted = f"{f:,.2f}"
    return f"{sym} {formatted}" if sym else formatted


def _fmt_float_ptbr(v: float | None) -> str:
    if v is None:
        return "(não informado)"
    return f"{v:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _fmt_float_en(v: float | None) -> str:
    if v is None:
        return "(not specified)"
    return f"{v:,.2f}"


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
    # Detect language for followups
    language = _detect_language(doc)
    
    if language == "en":
        base = "this document"
        outs: list[str] = []
        if doc.items:
            outs.append(f"Would you like me to export the items from {base} to CSV?")
        if doc.doc_type == "invoice":
            outs.append("Would you like me to validate the taxes and discounts provided?")
        if doc.doc_type == "purchase_order":
            outs.append("I can cross-reference with receipts to check for discrepancies.")
        if not outs:
            outs.append(
                "I can detail more fields (dates, conditions) or compare with other documents."
            )
        return outs
    else:
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
