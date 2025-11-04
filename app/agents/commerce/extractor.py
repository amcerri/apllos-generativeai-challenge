"""
Commerce document extractor (structured normalization).

Overview
--------
Turn raw commercial document text (PDF/DOCX extracted text) into a canonical
structured schema suitable for downstream summarization and risk checks. The
extractor is **dependency-light** and works heuristically, with an optional LLM
structured-output path (OpenAI) when available. It aims to be conservative and
never mutates external state.

Design
------
- Input: plain `text` plus optional `source_filename`, `source_mime`, and
  hints (`doc_type_hint`, `currency_hint`).
- Output: a `CommerceDoc` dataclass containing normalized fields:
  - `doc`, `buyer`, `vendor`, `event`, `dates`, `shipping`, `items[]`,
    `totals`, `terms`, `signatures`, `risks`, `meta`.
- Heuristics first: regex-based extraction for `doc_id`, currency detection,
  item rows, and totals. Approximate arithmetic checks (sum of lines ≈ subtotal
  and ≈ grand total) produce **non-fatal** risks.
- Optional LLM: a structured-output call can be enabled via `use_llm=True` when
  `OPENAI_API_KEY` is set; otherwise, the extractor falls back to the
  deterministic path.

Integration
-----------
- Used by the `commerce` agent between the detector and the summarizer.
- Logging uses the centralized infra if available; tracing spans are optional.
- The dataclasses are serializable via `.to_dict()` for easy transport.

Usage
-----
>>> from app.agents.commerce.extractor import CommerceExtractor
>>> ex = CommerceExtractor()
>>> doc = ex.extract(text="Invoice #INV-001\nItem A 2 10.00 20.00\nTotal USD 20.00", source_filename="invoice.pdf")
>>> doc.doc.doc_type, doc.doc.doc_id, doc.totals.grand_total
('invoice', 'INV-001', 20.0)
"""

from __future__ import annotations

import math
import os
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Final

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - fallback
        return _logging.getLogger(component)


# Tracing (optional; single alias)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: Mapping[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

__all__ = [
    "CommerceItem",
    "CommerceTotals",
    "CommerceTerms",
    "CommerceSignatures",
    "CommerceDocHeader",
    "CommerceDoc",
    "CommerceExtractor",
]


# ---------------------------------------------------------------------------
# Contracts (canonical schema)
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class CommerceItem:
    line_no: int | None
    sku: str | None
    name: str | None
    description: str | None
    qty: float | None
    unit: str | None
    unit_price: float | None
    taxes: list[dict[str, Any]]
    line_total: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "line_no": self.line_no,
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "qty": self.qty,
            "unit": self.unit,
            "unit_price": self.unit_price,
            "taxes": [dict(t) for t in self.taxes],
            "line_total": self.line_total,
        }


@dataclass(slots=True)
class CommerceTotals:
    subtotal: float | None
    discounts: list[dict[str, Any]]
    taxes: list[dict[str, Any]]
    freight: float | None
    other_charges: list[dict[str, Any]]
    grand_total: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "subtotal": self.subtotal,
            "discounts": [dict(d) for d in self.discounts],
            "taxes": [dict(t) for t in self.taxes],
            "freight": self.freight,
            "other_charges": [dict(o) for o in self.other_charges],
            "grand_total": self.grand_total,
        }


@dataclass(slots=True)
class CommerceTerms:
    payment_terms: str | None
    installments: str | None
    notes: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "payment_terms": self.payment_terms,
            "installments": self.installments,
            "notes": self.notes,
        }


@dataclass(slots=True)
class CommerceSignatures:
    customer_signed_at: str | None
    approver_signed_at: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_signed_at": self.customer_signed_at,
            "approver_signed_at": self.approver_signed_at,
        }


@dataclass(slots=True)
class CommerceDocHeader:
    doc_type: str | None
    doc_id: str | None
    source_filename: str | None
    source_mime: str | None
    extracted_at: str
    currency: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_type": self.doc_type,
            "doc_id": self.doc_id,
            "source_filename": self.source_filename,
            "source_mime": self.source_mime,
            "extracted_at": self.extracted_at,
            "currency": self.currency,
        }


@dataclass(slots=True)
class CommerceDoc:
    doc: CommerceDocHeader
    buyer: dict[str, Any]
    vendor: dict[str, Any]
    event: dict[str, Any]
    dates: dict[str, Any]
    shipping: dict[str, Any]
    items: list[CommerceItem]
    totals: CommerceTotals
    terms: CommerceTerms
    signatures: CommerceSignatures
    risks: list[str]
    meta: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc": self.doc.to_dict(),
            "buyer": dict(self.buyer),
            "vendor": dict(self.vendor),
            "event": dict(self.event),
            "dates": dict(self.dates),
            "shipping": dict(self.shipping),
            "items": [i.to_dict() for i in self.items],
            "totals": self.totals.to_dict(),
            "terms": self.terms.to_dict(),
            "signatures": self.signatures.to_dict(),
            "risks": list(self.risks),
            "meta": dict(self.meta),
        }


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------
class CommerceExtractor:
    """Normalize commerce documents using heuristics with optional LLM assist."""

    RE_DOC_ID = {
        "invoice": re.compile(
            r"\b(?:invoice\s*(?:no\.|#|number|nº)?\s*[:\-]?\s*)([A-Z0-9][A-Z0-9\-\./]{2,})",
            re.IGNORECASE,
        ),
        "purchase_order": re.compile(
            r"\b(?:po\s*(?:no\.|#|number|nº)?|purchase\s+order)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\./]{2,})",
            re.IGNORECASE,
        ),
        "order_form": re.compile(
            r"\border\s*form\b.*?\b(?:id|#|no\.)\s*[:\-]?\s*([A-Z0-9\-]{3,})", re.IGNORECASE
        ),
        "beo": re.compile(
            r"\b(?:banquet\s+event\s+order|beo)\b.*?\b(?:id|#|no\.)\s*[:\-]?\s*([A-Z0-9\-]{3,})",
            re.IGNORECASE,
        ),
        "receipt": re.compile(
            r"\breceipt\b.*?\b(?:id|#|no\.)\s*[:\-]?\s*([A-Z0-9\-]{3,})", re.IGNORECASE
        ),
        "quote": re.compile(
            r"\b(?:quote|quotation)\b.*?\b(?:id|#|no\.)\s*[:\-]?\s*([A-Z0-9\-]{3,})", re.IGNORECASE
        ),
    }

    RE_CURRENCY_SYM = re.compile(r"(US\$|U\$S|R\$|\$|€|£)")
    RE_CURRENCY_CODE = re.compile(r"\b(USD|BRL|EUR|GBP|ARS|CLP|MXN)\b", re.IGNORECASE)

    _CURRENCY_PREFIX = r"(?:US\$|U\$S|R\$|\$|€|£)\s*"

    RE_DATE = re.compile(r"\b((?:\d{4}[-/]\d{2}[-/]\d{2})|(?:\d{2}[-/]\d{2}[-/]\d{4}))\b")

    RE_TOTAL = re.compile(
        rf"\b(grand\s+total|total\s+geral|valor\s+total|total)\b[:\-]?\s*({_CURRENCY_PREFIX}?[0-9][0-9.,]*)",
        re.IGNORECASE,
    )
    RE_SUBTOTAL = re.compile(
        rf"\b(subtotal)\b[:\-]?\s*({_CURRENCY_PREFIX}?[0-9][0-9.,]*)",
        re.IGNORECASE,
    )
    RE_FREIGHT = re.compile(
        rf"\b(freight|shipping|frete)\b[:\-]?\s*({_CURRENCY_PREFIX}?[0-9][0-9.,]*)",
        re.IGNORECASE,
    )
    RE_DISCOUNT = re.compile(
        rf"\b(discount|desconto)\b[:\-]?\s*({_CURRENCY_PREFIX}?[0-9][0-9.,]*)",
        re.IGNORECASE,
    )

    RE_ITEM_LINE = re.compile(
        rf"^(?P<idx>\d{{1,4}})?\s*\)?\s*(?P<sku>[A-Z0-9_\-]{{3,}})?\s*(?P<name>[\w\- ,./]{{3,}})\s+(?:qty:)?(?P<qty>\d+[\.,]?\d*)\s+(?:unit:)?(?P<unit_price>{_CURRENCY_PREFIX}?[0-9][\d.,]*)\s+(?:line:)?(?P<line_total>{_CURRENCY_PREFIX}?[0-9][\d.,]*)\s*$",
        re.IGNORECASE,
    )

    DEFAULT_MAX_ITEMS: Final[int] = 100

    def __init__(self) -> None:
        self.log = get_logger("agent.commerce.extractor")

    def extract(
        self,
        *,
        text: str,
        source_filename: str | None = None,
        source_mime: str | None = None,
        doc_type_hint: str | None = None,
        currency_hint: str | None = None,
        use_llm: bool = False,
        max_items: int | None = None,
    ) -> dict[str, Any]:
        """Return a normalized :class:`CommerceDoc` from the given text.

        The LLM path is optional and only used when `use_llm=True` **and** an
        API key is configured. Otherwise a deterministic heuristic path is used.
        """

        with start_span("agent.commerce.extract", {"use_llm": use_llm}):
            text = (text or "").strip()
            if not text:
                doc = self._empty_doc(
                    source_filename=source_filename,
                    source_mime=source_mime,
                    doc_type=doc_type_hint,
                    currency=currency_hint,
                    parse_engine="empty@1",
                    warnings=["empty_text"],
                )
                return doc.to_dict()

            api_key = os.getenv("OPENAI_API_KEY")
            if use_llm and api_key:  # optional branch
                try:
                    doc = self._extract_via_llm(
                        text=text,
                        source_filename=source_filename,
                        source_mime=source_mime,
                        doc_type_hint=doc_type_hint,
                        currency_hint=currency_hint,
                    )
                    return doc.to_dict()
                except Exception as exc:
                    # Fall back to heuristics, attach warning
                    doc = self._extract_via_heuristics(
                        text=text,
                        source_filename=source_filename,
                        source_mime=source_mime,
                        doc_type_hint=doc_type_hint,
                        currency_hint=currency_hint,
                        max_items=max_items,
                    )
                    doc.risks = [*doc.risks, f"llm_extract_error:{type(exc).__name__}"]
                    return doc.to_dict()

            doc = self._extract_via_heuristics(
                text=text,
                source_filename=source_filename,
                source_mime=source_mime,
                doc_type_hint=doc_type_hint,
                currency_hint=currency_hint,
                max_items=max_items,
            )
            return doc.to_dict()

    # -- Paths ---------------------------------------------------------------
    def _extract_via_heuristics(
        self,
        *,
        text: str,
        source_filename: str | None,
        source_mime: str | None,
        doc_type_hint: str | None,
        currency_hint: str | None,
        max_items: int | None,
    ) -> CommerceDoc:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        tl = text.lower()

        doc_type = doc_type_hint or _guess_doc_type(tl)
        doc_id = _find_doc_id(text, doc_type)
        currency = currency_hint or _guess_currency(text)

        items = _parse_items(lines, currency, max_items or self.DEFAULT_MAX_ITEMS)
        totals = _parse_totals(text, currency)

        # Arithmetic checks
        risks: list[str] = []
        sum_lines = sum(i.line_total or 0.0 for i in items)
        if totals.subtotal is not None and not _approx_equal(sum_lines, totals.subtotal):
            risks.append("sum_lines_neq_subtotal")
        if totals.grand_total is not None:
            approx_sum = (totals.subtotal or sum_lines) + (totals.freight or 0.0)
            approx_sum -= sum(d.get("value", 0.0) for d in totals.discounts)
            approx_sum += sum(t.get("value", 0.0) for t in totals.taxes)
            approx_sum += sum(o.get("value", 0.0) for o in totals.other_charges)
            if not _approx_equal(approx_sum, totals.grand_total):
                risks.append("components_neq_grand_total")

        header = CommerceDocHeader(
            doc_type=doc_type,
            doc_id=doc_id,
            source_filename=source_filename,
            source_mime=source_mime,
            extracted_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
            currency=currency,
        )

        # Reconcile totals and append any risks
        recon_risks = _reconcile_totals(items, totals)

        return CommerceDoc(
            doc=header,
            buyer={},
            vendor={},
            event={},
            dates=_extract_dates(lines),
            shipping={},
            items=items,
            totals=totals,
            terms=CommerceTerms(payment_terms=None, installments=None, notes=None),
            signatures=CommerceSignatures(customer_signed_at=None, approver_signed_at=None),
            risks=list({*risks, *recon_risks}),
            meta={"parse_engine": "heuristic@1"},
        )

    def _extract_via_llm(
        self,
        *,
        text: str,
        source_filename: str | None,
        source_mime: str | None,
        doc_type_hint: str | None,
        currency_hint: str | None,
    ) -> CommerceDoc:  # best-effort; deterministic shape
        # Minimal structured-output prompt; remain conservative
        from app.infra.llm_client import get_llm_client

        client = get_llm_client()
        if not client.is_available():
            raise RuntimeError("LLM client not available")
        system = (
            "You are a careful information extractor. Return a strict JSON object "
            "conforming to the provided schema. Do not add fields."
        )
        schema = {
            "type": "object",
            "properties": {
                "doc_type": {"type": ["string", "null"]},
                "doc_id": {"type": ["string", "null"]},
                "currency": {"type": ["string", "null"]},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "line_no": {"type": ["integer", "null"]},
                            "sku": {"type": ["string", "null"]},
                            "name": {"type": ["string", "null"]},
                            "description": {"type": ["string", "null"]},
                            "qty": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "unit_price": {"type": ["number", "null"]},
                            "line_total": {"type": ["number", "null"]},
                        },
                        "additionalProperties": False,
                    },
                },
                "totals": {
                    "type": "object",
                    "properties": {
                        "subtotal": {"type": ["number", "null"]},
                        "freight": {"type": ["number", "null"]},
                        "grand_total": {"type": ["number", "null"]},
                    },
                    "additionalProperties": True,
                },
            },
            "required": ["items", "totals"],
            "additionalProperties": True,
        }
        user = (
            f"Text (first 6000 chars):\n{text[:6000]}\n\n"
            f"Hints: doc_type={doc_type_hint!r}, currency={currency_hint!r}."
        )

        resp = client.chat_completion(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            model="gpt-4.1",
            temperature=0,
            response_format={"type": "json_schema", "json_schema": {"name": "commerce_extract", "schema": schema}},
            max_retries=0,
        )
        raw = (resp.text if resp else "")
        try:
            from json import loads as _loads
            data = client.extract_json(raw) or {}
            if not data:
                data = _loads(raw) if raw else {}
        except Exception:
            data = {}

        doc_type = data.get("doc_type") or doc_type_hint
        currency = data.get("currency") or currency_hint or _guess_currency(text)
        doc_id = data.get("doc_id") or _find_doc_id(text, doc_type)

        items: list[CommerceItem] = []
        for i, it in enumerate(data.get("items", [])[: self.DEFAULT_MAX_ITEMS], start=1):
            items.append(
                CommerceItem(
                    line_no=_as_int(it.get("line_no")) or i,
                    sku=_as_str(it.get("sku")),
                    name=_as_str(it.get("name")),
                    description=_as_str(it.get("description")),
                    qty=_as_float(it.get("qty")),
                    unit=_as_str(it.get("unit")),
                    unit_price=_as_float(it.get("unit_price")),
                    taxes=[],
                    line_total=_as_float(it.get("line_total")),
                )
            )

        totals_map = data.get("totals", {})
        totals = CommerceTotals(
            subtotal=_as_float(totals_map.get("subtotal")),
            discounts=[],
            taxes=[],
            freight=_as_float(totals_map.get("freight")),
            other_charges=[],
            grand_total=_as_float(totals_map.get("grand_total")),
        )

        header = CommerceDocHeader(
            doc_type=doc_type,
            doc_id=doc_id,
            source_filename=source_filename,
            source_mime=source_mime,
            extracted_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
            currency=currency,
        )

        return CommerceDoc(
            doc=header,
            buyer={},
            vendor={},
            event={},
            dates=_extract_dates([ln.strip() for ln in text.splitlines() if ln.strip()]),
            shipping={},
            items=items,
            totals=totals,
            terms=CommerceTerms(payment_terms=None, installments=None, notes=None),
            signatures=CommerceSignatures(customer_signed_at=None, approver_signed_at=None),
            risks=[],
            meta={"parse_engine": "openai-structured@4.1"},
        )

    def _empty_doc(
        self,
        *,
        source_filename: str | None,
        source_mime: str | None,
        doc_type: str | None,
        currency: str | None,
        parse_engine: str,
        warnings: Sequence[str],
    ) -> CommerceDoc:
        header = CommerceDocHeader(
            doc_type=doc_type,
            doc_id=None,
            source_filename=source_filename,
            source_mime=source_mime,
            extracted_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
            currency=currency,
        )
        totals = CommerceTotals(
            subtotal=None, discounts=[], taxes=[], freight=None, other_charges=[], grand_total=None
        )
        return CommerceDoc(
            doc=header,
            buyer={},
            vendor={},
            event={},
            dates={},
            shipping={},
            items=[],
            totals=totals,
            terms=CommerceTerms(payment_terms=None, installments=None, notes=None),
            signatures=CommerceSignatures(customer_signed_at=None, approver_signed_at=None),
            risks=list(warnings),
            meta={"parse_engine": parse_engine},
        )


# ---------------------------------------------------------------------------
# Heuristic helpers
# ---------------------------------------------------------------------------


def _guess_doc_type(tl: str) -> str | None:
    """Best-effort document type guess from lowercased text.

    Parameters
    ----------
    tl : str
        Lowercased full text.

    Returns
    -------
    str | None
        One of known doc types or None when no clear hint is present.
    """
    if "invoice" in tl or "fatura" in tl or "nota fiscal" in tl:
        return "invoice"
    if "purchase order" in tl or re.search(r"\bpo\b", tl):
        return "purchase_order"
    if "banquet event order" in tl or re.search(r"\bbeo\b", tl):
        return "beo"
    if "order form" in tl:
        return "order_form"
    if "receipt" in tl or "recibo" in tl:
        return "receipt"
    if "quote" in tl or "quotation" in tl or "orçamento" in tl or "orcamento" in tl:
        return "quote"
    return None


def _find_doc_id(text: str, doc_type: str | None) -> str | None:
    """Extract a plausible document identifier based on the doc_type.

    Falls back to trying all known patterns when doc_type is unknown.
    """
    if not doc_type:
        # try all patterns
        for rx in CommerceExtractor.RE_DOC_ID.values():
            m = rx.search(text)
            if m:
                return m.group(1).strip().strip(".:#")
        return None
    pattern = CommerceExtractor.RE_DOC_ID.get(doc_type)
    if pattern is None:
        return None
    m = pattern.search(text)
    return m.group(1).strip().strip(".:#") if m else None


def _guess_currency(text: str) -> str | None:
    """Guess currency code from symbol or explicit ISO-4217 codes in text."""
    m_code = CommerceExtractor.RE_CURRENCY_CODE.search(text)
    if m_code:
        return m_code.group(1).upper()
    m_sym = CommerceExtractor.RE_CURRENCY_SYM.search(text)
    if not m_sym:
        return None
    sym = m_sym.group(1)
    if sym == "R$":
        return "BRL"
    if sym == "€":
        return "EUR"
    if sym == "£":
        return "GBP"
    if sym == "$":
        return "USD"
    return None


def _parse_amount(s: str, currency: str | None) -> float | None:
    """Parse a localized numeric amount into float.

    Handles common thousand/decimal separator conventions.
    """
    # Normalize thousand/decimal separators for common locales
    s = s.strip()
    s = re.sub(r"^[^0-9\-]*", "", s)  # drop leading symbols/currency
    if not s:
        return None
    # If both comma and dot present: assume dot thousands + comma decimal (pt-BR)
    if "," in s and "." in s:
        s2 = s.replace(".", "").replace(",", ".")
    elif "," in s and "." not in s:
        # only comma: treat as decimal separator
        s2 = s.replace(",", ".")
    else:
        s2 = s
    try:
        return float(s2)
    except Exception:
        return None


def _parse_items(lines: Sequence[str], currency: str | None, max_items: int) -> list[CommerceItem]:
    """Parse line items from structured lines matching item regex.

    Derives missing numeric fields when two of the three (qty, unit_price,
    line_total) are present.
    """
    items: list[CommerceItem] = []
    for ln in lines:
        m = CommerceExtractor.RE_ITEM_LINE.match(ln)
        if not m:
            continue
        idx = _as_int(m.group("idx"))
        sku = _as_str(m.group("sku"))
        name = _as_str(m.group("name"))
        qty = _parse_amount(m.group("qty") or "", currency)
        unit_price = _parse_amount(m.group("unit_price") or "", currency)
        line_total = _parse_amount(m.group("line_total") or "", currency)

        # Consistency: if two of three numbers exist, derive the third
        if qty is not None and unit_price is not None and line_total is None:
            line_total = round(qty * unit_price, 2)
        if line_total is not None and unit_price is not None and qty is None and unit_price != 0:
            qty = round(line_total / unit_price, 4)
        if line_total is not None and qty is not None and unit_price is None and qty != 0:
            unit_price = round(line_total / qty, 4)

        items.append(
            CommerceItem(
                line_no=idx,
                sku=sku,
                name=name,
                description=None,
                qty=qty,
                unit=None,
                unit_price=unit_price,
                taxes=[],
                line_total=line_total,
            )
        )
        if len(items) >= max_items:
            break
    return items


def _parse_totals(text: str, currency: str | None) -> CommerceTotals:
    """Parse subtotal, freight, discounts, and grand total from text."""
    subtotal = None
    grand = None
    freight = None
    discounts: list[dict[str, Any]] = []
    taxes: list[dict[str, Any]] = []
    others: list[dict[str, Any]] = []

    m = CommerceExtractor.RE_SUBTOTAL.search(text)
    if m:
        subtotal = _parse_amount(m.group(2), currency)

    m = CommerceExtractor.RE_FREIGHT.search(text)
    if m:
        freight = _parse_amount(m.group(2), currency)

    for dm in CommerceExtractor.RE_DISCOUNT.finditer(text):
        val = _parse_amount(dm.group(2), currency)
        if val is not None:
            discounts.append({"label": dm.group(1).lower(), "value": val})

    m = CommerceExtractor.RE_TOTAL.search(text)
    if m:
        grand = _parse_amount(m.group(2), currency)

    return CommerceTotals(
        subtotal=subtotal,
        discounts=discounts,
        taxes=taxes,
        freight=freight,
        other_charges=others,
        grand_total=grand,
    )


def _extract_dates(lines: Sequence[str]) -> dict[str, Any]:
    """Extract best-effort issue and due dates from the first two matches."""
    # Best-effort: pick first two dates as issue/due
    found: list[str] = []
    for ln in lines:
        for m in CommerceExtractor.RE_DATE.finditer(ln):
            found.append(m.group(1))
            if len(found) >= 2:
                break
        if len(found) >= 2:
            break
    issue = _normalize_date(found[0]) if len(found) >= 1 else None
    due = _normalize_date(found[1]) if len(found) >= 2 else None
    return {"issue_date": issue, "due_date": due}


def _reconcile_totals(items: list[CommerceItem], totals: CommerceTotals) -> list[str]:
    """Return risk codes for inconsistencies between items and totals.

    Parameters
    ----------
    items : list[CommerceItem]
        Parsed line items with numeric amounts where available.
    totals : CommerceTotals
        Totals parsed from the document.

    Returns
    -------
    list[str]
        A list of risk codes, empty when no issues detected.
    """

    risks: list[str] = []
    sum_lines = sum(i.line_total or 0.0 for i in items)
    if totals.subtotal is not None and not _approx_equal(sum_lines, totals.subtotal):
        risks.append("sum_lines_neq_subtotal")
    if totals.grand_total is not None:
        approx_sum = (totals.subtotal or sum_lines) + (totals.freight or 0.0)
        approx_sum -= sum(d.get("value", 0.0) for d in totals.discounts)
        approx_sum += sum(t.get("value", 0.0) for t in totals.taxes)
        approx_sum += sum(o.get("value", 0.0) for o in totals.other_charges)
        if not _approx_equal(approx_sum, totals.grand_total):
            risks.append("components_neq_grand_total")
    return risks


def _normalize_date(s: str | None) -> str | None:
    """Normalize a variety of date formats to YYYY-MM-DD when possible."""
    if not s:
        return None
    # Try ISO first
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
            return s
        if re.match(r"^\d{4}/\d{2}/\d{2}$", s):
            y, m, d = s.split("/")
            return f"{y}-{m}-{d}"
        if re.match(r"^\d{2}-\d{2}-\d{4}$", s) or re.match(r"^\d{2}/\d{2}/\d{4}$", s):
            sep = "-" if "-" in s else "/"
            d, m, y = s.split(sep)
            return f"{y}-{m}-{d}"
    except Exception:
        return None
    return s


def _approx_equal(a: float, b: float, *, rel: float = 1e-3, abs_: float = 0.05) -> bool:
    """Compare two floats using relative and absolute tolerances."""
    if math.isfinite(a) and math.isfinite(b):
        return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b)))
    return False


def _as_str(v: Any) -> str | None:
    """Return stripped string or None when empty/None."""
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _as_int(v: Any) -> int | None:
    """Parse int or return None on failure."""
    try:
        return int(str(v).strip())
    except Exception:
        return None


def _as_float(v: Any) -> float | None:
    """Parse float or return None on failure."""
    try:
        return float(v)
    except Exception:
        return None
