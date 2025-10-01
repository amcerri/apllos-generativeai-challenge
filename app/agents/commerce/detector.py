"""
Commerce document detector (heuristic, safe, dependency-light).

Overview
--------
Detects whether an input document (PDF/DOCX text) is a commercial document and
infers its `doc_type` (e.g., `invoice`, `purchase_order`, `order_form`, `beo`).
The detector uses conservative keyword/layout hints, optional filename/mime
signals, and extracts a likely `doc_id` and `currency` when present. It returns
an immutable result dataclass for downstream extraction/normalization.

Design
------
- Signals: keyword matches (titles/labels), filename/mime hints, id patterns,
  currency symbols/codes.
- Scoring: per-type score ∈ [0..1] from weighted signals; top type is selected.
- Safety: pure-Python, no external I/O; no DML/DDL; robust to missing fields.
- Dependencies: standard library only; logging/tracing are optional fallbacks.

Integration
-----------
- Call from the commerce agent before the extractor. Example:

>>> from app.agents.commerce.detector import CommerceDetector
>>> det = CommerceDetector()
>>> res = det.detect(source_filename="invoice_123.pdf", source_mime="application/pdf", text="Invoice #INV-001 Total USD 120.00")
>>> res.doc_type, res.doc_id, res.currency
('invoice', 'INV-001', 'USD')

Usage
-----
Provide either `text` (extracted OCR/plaintext) or rely on filename/mime hints.
When both exist, text dominates.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Final

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - simple fallback
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

__all__ = ["DetectionResult", "CommerceDetector"]


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class DetectionResult:
    """Immutable detection outcome for commerce docs.

    Attributes
    ----------
    doc_type: One of {"invoice", "purchase_order", "order_form", "beo", "receipt", "quote"} or None.
    confidence: Detector confidence in [0..1].
    doc_id: Extracted identifier like Invoice/PO number (best effort).
    currency: ISO code like "USD", "BRL", "EUR" when detectable.
    signals: List of human-readable detection signals.
    warnings: Non-fatal notes (e.g., ambiguous currency symbol).
    meta: Arbitrary diagnostics (e.g., detector version).
    """

    doc_type: str | None
    confidence: float
    doc_id: str | None
    currency: str | None
    signals: list[str]
    warnings: list[str]
    meta: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:  # noqa: D401 - straightforward mapping
        return {
            "doc_type": self.doc_type,
            "confidence": self.confidence,
            "doc_id": self.doc_id,
            "currency": self.currency,
            "signals": list(self.signals),
            "warnings": list(self.warnings),
            "meta": dict(self.meta),
        }


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------
class CommerceDetector:
    """Heuristic detector for commerce document types."""

    # Simple keyword sets per type (lowercase)
    KW: Final[dict[str, tuple[str, ...]]] = {
        "invoice": (
            "invoice",
            "nota fiscal",
            "nota fiscal eletrônica",
            "nfe",
            "nf-e",
            "fatura",
            "danfe",
            "bill to",
            "invoice number",
            "amount due",
        ),
        "purchase_order": (
            "purchase order",
            "po number",
            "po no",
            "pedido de compra",
            "buyer:",
        ),
        "order_form": (
            "order form",
            "customer order",
            "order details",
            "order information",
        ),
        "beo": (
            "banquet event order",
            "beo",
            "event details",
            "function date",
            "banquet",
        ),
        "receipt": (
            "receipt",
            "recibo",
            "sales receipt",
            "approved",
            "payment method",
        ),
        "quote": (
            "quote",
            "quotation",
            "orçamento",
            "orcamento",
            "valid until",
        ),
    }

    # Doc ID patterns (capture group 1 is the ID)
    RE_ID: Final[dict[str, re.Pattern[str]]] = {
        "invoice": re.compile(
            r"\b(?:(?:invoice|nota\s+fiscal(?:\s+eletr[ôo]nica)?|nf-?e)\s*(?:no\.|#|number|nº)?\s*[:\-]?\s*)([A-Z0-9][A-Z0-9\-\./]{2,})",
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

    # Currency
    RE_CURR_SYM: Final[re.Pattern[str]] = re.compile(r"(US\$\s?|R\$\s?|\$|€|£)")
    RE_CURR_CODE: Final[re.Pattern[str]] = re.compile(
        r"\b(USD|BRL|EUR|GBP|ARS|CLP|MXN)\b", re.IGNORECASE
    )

    def __init__(self) -> None:
        self.log = get_logger("agent.commerce.detector")

    # Public API -------------------------------------------------------------
    def detect(
        self,
        *,
        source_filename: str | None = None,
        source_mime: str | None = None,
        text: str | None = None,
    ) -> DetectionResult:
        """Return a :class:`DetectionResult` with type, id, currency and signals."""

        with start_span("agent.commerce.detect"):
            signals: list[str] = []
            warnings: list[str] = []

            t = (text or "").strip()
            tl = t.lower()
            fname = (source_filename or "").lower()
            mime = (source_mime or "").lower()

            # Score by keywords
            type_scores: dict[str, float] = {}
            for dtype, kws in self.KW.items():
                hits = sum(1 for kw in kws if kw in tl)
                if hits:
                    signals.append(f"kw:{dtype}:{hits}")
                # normalize by number of keywords for that type
                type_scores[dtype] = min(1.0, hits / max(3.0, float(len(kws))))

            # Filename/mime hints
            for dtype in self.KW.keys():
                if dtype in fname:
                    type_scores[dtype] = max(type_scores.get(dtype, 0.0), 0.4)
                    signals.append(f"fname:{dtype}")
            if "pdf" in mime or "msword" in mime or "officedocument" in mime:
                signals.append("mime:doc")

            # Doc id extraction (evaluate per type; keep first successful)
            doc_id: str | None = None
            for dtype, rx in self.RE_ID.items():
                m = rx.search(t)
                if m:
                    doc_id = m.group(1).strip().strip(".:#")
                    type_scores[dtype] = max(type_scores.get(dtype, 0.0), 0.75)
                    signals.append(f"id:{dtype}")
                    break

            # Currency
            currency: str | None = None
            codes = [c.upper() for c in self.RE_CURR_CODE.findall(t)]
            syms = [s.strip() for s in self.RE_CURR_SYM.findall(t)]
            if codes:
                uniq = sorted(set(codes))
                if len(uniq) > 1:
                    warnings.append(f"ambiguous_currency_codes:{','.join(uniq[:4])}")
                for pref in ("USD", "BRL", "EUR", "GBP"):
                    if pref in uniq:
                        currency = pref
                        break
                currency = currency or uniq[0]
                signals.append(f"ccy:{currency}")
            elif syms:
                mapped: list[str] = []
                for sym in syms:
                    sym = sym.replace(" ", "")
                    if sym == "R$":
                        mapped.append("BRL")
                    elif sym in ("US$", "$"):
                        mapped.append("USD")
                    elif sym == "€":
                        mapped.append("EUR")
                    elif sym == "£":
                        mapped.append("GBP")
                if mapped:
                    uniq = sorted(set(mapped))
                    if len(uniq) > 1:
                        warnings.append(f"ambiguous_currency_symbol:{','.join(uniq[:4])}")
                    currency = ("USD" if "USD" in uniq else uniq[0])
                    signals.append(f"ccy_sym:{'/'.join(syms[:2])}")

            # Choose the best type
            best_type: str | None = None
            best_score = 0.0
            for dtype, sc in type_scores.items():
                if sc > best_score:
                    best_type, best_score = dtype, sc

            # Confidence shaping: add small boosts for id/currency presence
            if doc_id:
                best_score = min(1.0, best_score + 0.15)
            if currency:
                best_score = min(1.0, best_score + 0.05)

            # If everything is weak and we have no text, fall back to filename
            if (
                not t
                and best_score < 0.5
                and any(k in fname for k in ("invoice", "po", "order", "beo"))
            ):
                if "invoice" in fname:
                    best_type, best_score = "invoice", 0.55
                elif "po" in fname or "purchase" in fname:
                    best_type, best_score = "purchase_order", 0.55
                elif "order" in fname:
                    best_type, best_score = "order_form", 0.5
                elif "beo" in fname:
                    best_type, best_score = "beo", 0.6

            result = DetectionResult(
                doc_type=best_type,
                confidence=float(round(best_score, 3)),
                doc_id=doc_id,
                currency=currency,
                signals=signals,
                warnings=warnings,
                meta={"detector": "heuristic@1"},
            )

            # Log a concise summary
            try:
                self.log.info(
                    "Commerce detection",
                    doc_type=result.doc_type,
                    confidence=result.confidence,
                    currency=result.currency,
                    has_id=bool(result.doc_id),
                    signals=",".join(result.signals[:6]),
                )
            except Exception:
                pass

            return result
