"""
Commerce document extractor (LLM-powered structured extraction).

Overview
--------
Extract structured data from commercial documents using OpenAI's structured
output capabilities. This extractor is designed to be the primary extraction
method, replacing heuristic-based approaches with LLM intelligence for better
accuracy across diverse document formats and layouts.

Design
------
- Input: plain text (from DocumentProcessor), metadata, and optional hints
- Output: structured CommerceDoc following canonical schema
- LLM-first: uses OpenAI with JSON Schema for reliable structured output
- No fallbacks: designed to be robust enough to handle all cases
- Enhanced prompting: includes business insights and risk analysis

Integration
-----------
- Used by the commerce agent after DocumentProcessor
- Logging uses centralized infra if available; tracing spans are optional
- Returns structured data compatible with existing commerce pipeline

Usage
-----
>>> from app.agents.commerce.extractor_llm import LLMCommerceExtractor
>>> extractor = LLMCommerceExtractor()
>>> result = extractor.extract(
...     text="Invoice #INV-001\nItem A: 2x $10.00 = $20.00\nTotal: $20.00",
...     metadata={"filename": "invoice.pdf", "method": "pdf_direct"}
... )
>>> result["doc"]["doc_type"], result["totals"]["grand_total"]
('invoice', 20.0)
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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


# Optional OpenAI client
openai: Any = None
try:
    import openai as _openai
    openai = _openai
except Exception:  # pragma: no cover - optional
    pass


__all__ = ["LLMCommerceExtractor"]


# ---------------------------------------------------------------------------
# LLM Commerce Extractor
# ---------------------------------------------------------------------------
class LLMCommerceExtractor:
    """Extract structured commerce data using LLM with JSON Schema."""

    def __init__(self) -> None:
        self.log = get_logger("agent.commerce.extractor_llm")
        self._config = get_config()
        self._system_prompt = self._load_system_prompt()
        self._json_schema = self._load_json_schema()

    def extract(
        self,
        *,
        text: str,
        metadata: dict[str, Any] | None = None,
        doc_type_hint: str | None = None,
        currency_hint: str | None = None,
    ) -> dict[str, Any]:
        """Extract structured data from document text using LLM.

        Parameters
        ----------
        text: Extracted text from document
        metadata: Processing metadata from DocumentProcessor
        doc_type_hint: Optional document type hint from detector
        currency_hint: Optional currency hint from detector

        Returns
        -------
        Structured commerce document following canonical schema
        """
        with start_span("agent.commerce.extract_llm"):
            text = (text or "").strip()
            metadata = metadata or {}
            
            if not text:
                return self._empty_document(metadata, ["empty_text"])
            
            # Check for OpenAI API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or openai is None:
                self.log.error("OpenAI API key not configured or openai package not available")
                return self._empty_document(metadata, ["no_openai_api"])
            
            try:
                return self._extract_with_openai(
                    text=text,
                    metadata=metadata,
                    doc_type_hint=doc_type_hint,
                    currency_hint=currency_hint,
                    api_key=api_key
                )
            except Exception as e:
                self.log.error("LLM extraction failed", error=str(e), text_length=len(text))
                return self._empty_document(metadata, [f"llm_error:{type(e).__name__}"])

    def _extract_with_openai(
        self,
        text: str,
        metadata: dict[str, Any],
        doc_type_hint: str | None,
        currency_hint: str | None,
        api_key: str,
    ) -> dict[str, Any]:
        """Perform extraction using OpenAI structured output."""
        
        # Build user message with context
        user_message = self._build_user_message(
            text=text,
            metadata=metadata,
            doc_type_hint=doc_type_hint,
            currency_hint=currency_hint
        )
        
        # Create OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Get configuration values with fallbacks
        if self._config is None:
            model = "gpt-4o-mini"
            temperature = 0.1
            max_tokens = 4000
            strict = False
        else:
            model = self._config.get_llm_model("commerce_extractor")
            temperature = self._config.get_llm_temperature("commerce_extractor")
            max_tokens = self._config.get_llm_max_tokens("commerce_extractor")
            strict = self._config.get("commerce.extraction.json_schema_strict", False)
        
        # Call OpenAI with structured output
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "commerce_document",
                    "schema": self._json_schema,
                    "strict": strict
                }
            },
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Parse response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")
        
        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        
        # Add metadata
        if "meta" not in result or result["meta"] is None:
            result["meta"] = {}
        
        result["meta"].update({
            "extraction_method": "llm_openai",
            "model": "gpt-4o-mini",
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "source_metadata": metadata,
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
        })
        
        # Ensure required fields
        if "doc" not in result:
            result["doc"] = {"doc_type": "unknown"}
        if "items" not in result:
            result["items"] = []
        if "totals" not in result:
            result["totals"] = {}
        if "risks" not in result:
            result["risks"] = []
        
        # Debug: log the extracted doc_type
        self.log.info("LLM extraction debug", 
                     doc_type=result["doc"].get("doc_type"),
                     doc_keys=list(result["doc"].keys()) if "doc" in result else None)
        
        # Add source info to doc section
        result["doc"].update({
            "source_filename": metadata.get("filename"),
            "source_mime": metadata.get("mime_type"),
            "extracted_at": result["meta"]["extracted_at"],
        })
        
        self.log.info(
            "LLM extraction completed",
            doc_type=result["doc"].get("doc_type"),
            items_count=len(result["items"]),
            risks_count=len(result["risks"]),
            tokens_used=response.usage.total_tokens if response.usage else None
        )
        
        return result

    def _build_user_message(
        self,
        text: str,
        metadata: dict[str, Any],
        doc_type_hint: str | None,
        currency_hint: str | None,
    ) -> str:
        """Build user message with document text and context."""
        
        parts = []
        
        # Add context information
        if metadata:
            parts.append("=== DOCUMENT METADATA ===")
            if metadata.get("filename"):
                parts.append(f"Filename: {metadata['filename']}")
            if metadata.get("method"):
                parts.append(f"Extraction method: {metadata['method']}")
            if metadata.get("pages"):
                parts.append(f"Pages: {metadata['pages']}")
            if metadata.get("warnings"):
                parts.append(f"Processing warnings: {', '.join(metadata['warnings'])}")
        
        # Add hints if available
        if doc_type_hint or currency_hint:
            parts.append("\n=== HINTS ===")
            if doc_type_hint:
                parts.append(f"Suggested document type: {doc_type_hint}")
            if currency_hint:
                parts.append(f"Suggested currency: {currency_hint}")
        
        # Add the main document text
        parts.append("\n=== DOCUMENT TEXT ===")
        parts.append(text)
        
        # Add extraction instructions
        parts.append("\n=== INSTRUCTIONS ===")
        parts.append("Extract all relevant information from this document and return a JSON object following the schema.")
        parts.append("Focus on:")
        parts.append("- Accurate document type identification")
        parts.append("- Complete item extraction with quantities and prices")
        parts.append("- Proper totals calculation and validation")
        parts.append("- Risk identification (calculation mismatches, missing data)")
        parts.append("- Business insights (delivery dates, payment terms, special conditions)")
        
        return "\n".join(parts)

    def _load_system_prompt(self) -> str:
        """Load system prompt from file."""
        try:
            prompt_path = Path(__file__).parent.parent.parent / "prompts" / "commerce" / "extractor_system.txt"
            return prompt_path.read_text(encoding="utf-8")
        except Exception as e:
            self.log.warning("Failed to load system prompt", error=str(e))
            return self._fallback_system_prompt()

    def _fallback_system_prompt(self) -> str:
        """Fallback system prompt if file loading fails."""
        return """You are a Commerce Document Extractor. Extract structured data from commercial documents and return JSON only.

Extract document type, buyer/vendor info, items with quantities and prices, totals, dates, and identify any risks or inconsistencies.

Return JSON following the canonical commerce document schema with proper data types and null values for missing fields."""

    def _load_json_schema(self) -> dict[str, Any]:
        """Load JSON schema for structured output."""
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "doc": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "doc_type": {"type": "string"},
                        "doc_id": {"type": ["string", "null"]},
                        "source_filename": {"type": ["string", "null"]},
                        "source_mime": {"type": ["string", "null"]},
                        "extracted_at": {"type": ["string", "null"]},
                        "currency": {"type": ["string", "null"]}
                    },
                    "required": ["doc_type", "doc_id", "source_filename", "source_mime", "extracted_at", "currency"]
                },
                "buyer": {"type": ["object", "null"]},
                "vendor": {"type": ["object", "null"]},
                "event": {"type": ["object", "null"]},
                "dates": {"type": ["object", "null"]},
                "shipping": {"type": ["object", "null"]},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "line_no": {"type": ["string", "integer", "null"]},
                            "sku": {"type": ["string", "null"]},
                            "name": {"type": ["string", "null"]},
                            "description": {"type": ["string", "null"]},
                            "qty": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "unit_price": {"type": ["number", "null"]},
                            "taxes": {"type": "array", "items": {"type": "object"}},
                            "line_total": {"type": ["number", "null"]}
                        }
                    }
                },
                "totals": {
                    "type": ["object", "null"],
                    "additionalProperties": False,
                    "properties": {
                        "subtotal": {"type": ["number", "null"]},
                        "discounts": {"type": "array", "items": {"type": "object"}},
                        "taxes": {"type": "array", "items": {"type": "object"}},
                        "freight": {"type": ["number", "null"]},
                        "other_charges": {"type": "array", "items": {"type": "object"}},
                        "grand_total": {"type": ["number", "null"]}
                    }
                },
                "terms": {
                    "type": ["object", "null"],
                    "additionalProperties": False,
                    "properties": {
                        "payment_terms": {"type": ["string", "null"]},
                        "installments": {"type": ["string", "null"]},
                        "notes": {"type": ["string", "null"]}
                    }
                },
                "signatures": {
                    "type": ["object", "null"],
                    "additionalProperties": False,
                    "properties": {
                        "customer_signed_at": {"type": ["string", "null"]},
                        "approver_signed_at": {"type": ["string", "null"]}
                    }
                },
                "risks": {"type": "array", "items": {"type": "string"}},
                "meta": {"type": ["object", "null"]}
            },
            "required": ["doc", "items", "totals", "risks"]
        }

    def _empty_document(self, metadata: dict[str, Any], warnings: list[str]) -> dict[str, Any]:
        """Return empty document structure with warnings."""
        return {
            "doc": {
                "doc_type": "unknown",
                "doc_id": None,
                "source_filename": metadata.get("filename"),
                "source_mime": metadata.get("mime_type"),
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "currency": None
            },
            "buyer": None,
            "vendor": None,
            "event": None,
            "dates": None,
            "shipping": None,
            "items": [],
            "totals": {
                "subtotal": None,
                "discounts": [],
                "taxes": [],
                "freight": None,
                "other_charges": [],
                "grand_total": None
            },
            "terms": None,
            "signatures": None,
            "risks": warnings,
            "meta": {
                "extraction_method": "empty",
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "source_metadata": metadata,
                "warnings": warnings
            }
        }
