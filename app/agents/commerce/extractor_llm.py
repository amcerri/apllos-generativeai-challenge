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
from typing import Any

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
                self.log.error(
                    "OpenAI API key not configured or openai package not available",
                    extra={}
                )
                # Fallback to heuristic extractor
                try:
                    from app.agents.commerce.extractor import CommerceExtractor as _HeuristicExtractor
                    hx = _HeuristicExtractor()
                    return hx.extract(
                        text=text,
                        source_filename=metadata.get("filename"),
                        source_mime=metadata.get("mime_type"),
                        doc_type_hint=doc_type_hint,
                        currency_hint=currency_hint,
                        use_llm=False,
                    )
                except Exception as eh:
                    self.log.warning(
                        "Heuristic fallback failed",
                        extra={"error": str(eh)}
                    )
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
                self.log.error(
                    "LLM extraction failed",
                    extra={"error": str(e), "text_length": len(text)}
                )
                # Fallback to heuristic extractor on error
                try:
                    from app.agents.commerce.extractor import CommerceExtractor as _HeuristicExtractor
                    hx = _HeuristicExtractor()
                    return hx.extract(
                        text=text,
                        source_filename=metadata.get("filename"),
                        source_mime=metadata.get("mime_type"),
                        doc_type_hint=doc_type_hint,
                        currency_hint=currency_hint,
                        use_llm=False,
                    )
                except Exception as eh:
                    self.log.warning(
                        "Heuristic fallback failed",
                        extra={"error": str(eh)}
                    )
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
        
        # Get configuration values with fallbacks
        if self._config is None:
            model = "gpt-4o-mini"
            temperature = 0.1
            max_tokens = 4000
            strict = False
            timeout_seconds = 180.0
        else:
            # Use centralized models config
            model = self._config.models.commerce_extractor.name
            temperature = self._config.models.commerce_extractor.temperature
            max_tokens = self._config.models.commerce_extractor.max_tokens
            strict = self._config.commerce.extraction.json_schema_strict
            timeout_seconds = float(self._config.models.commerce_extractor.timeout_seconds)
        
        # Get centralized LLM client, but create a custom one with proper timeout if needed
        from app.infra.llm_client import get_llm_client, LLMClient
        base_client = get_llm_client()
        
        if not base_client.is_available():
            raise ValueError("LLM client not available")
        
        # Create a client with the specific timeout for this model
        # Use the base client's settings but override timeout
        client = LLMClient(
            api_key=base_client.api_key,
            model=model,
            timeout=timeout_seconds,
            max_retries=base_client.max_retries,
            retry_delay=base_client.retry_delay
        )
        
        # Build messages and log sizes
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_message}
        ]
        system_prompt_size = len(self._system_prompt)
        user_message_size = len(user_message)
        total_chars = system_prompt_size + user_message_size
        
        # Log LLM extraction start with detailed metrics
        self.log.info("Starting LLM extraction", 
                     extra={
                         "model": model,
                         "timeout_seconds": timeout_seconds,
                         "max_tokens": max_tokens,
                         "text_length": len(text),
                         "system_prompt_size": system_prompt_size,
                         "user_message_size": user_message_size,
                         "total_chars": total_chars,
                         "estimated_tokens": total_chars // 4,  # Rough estimate: ~4 chars per token
                         "file_name": metadata.get("filename")
                     })
        
        import time
        start_time = time.time()
        
        # Call LLM with structured output
        response = client.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "commerce_document",
                    "schema": self._json_schema,
                    "strict": strict
                }
            },
            max_retries=0
        )
        
        elapsed_time = time.time() - start_time
        
        if response is None:
            self.log.error("Empty response from LLM", extra={"elapsed_seconds": elapsed_time, "file_name": metadata.get("filename")})
            raise ValueError("Empty response from LLM")
        
        self.log.info("LLM API call completed", 
                     extra={
                         "elapsed_seconds": round(elapsed_time, 2),
                         "response_length": len(response.text) if response.text else 0,
                         "tokens_used": response.usage.get("total_tokens") if response.usage else None,
                         "file_name": metadata.get("filename")
                     })
        
        # Parse response using centralized JSON extraction
        result = client.extract_json(response.text, schema=self._json_schema)
        if result is None:
            raise ValueError("Could not parse JSON from LLM response")
        
        # Add metadata
        if "meta" not in result or result["meta"] is None:
            result["meta"] = {}
        
        usage = response.usage or {}
        result["meta"].update({
            "extraction_method": "llm_openai",
            "model": "gpt-4o-mini",
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "source_metadata": metadata,
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
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
            tokens_used=(usage.get("total_tokens") if isinstance(usage, dict) else None)
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

        # Lightweight detector: derive hints from text when none provided
        if not doc_type_hint:
            tl = text.lower()
            if "invoice" in tl or "fatura" in tl or "nota fiscal" in tl:
                parts.append("Detected document type: invoice")
            elif "purchase order" in tl or " po " in tl:
                parts.append("Detected document type: purchase_order")
            elif "banquet event order" in tl or " beo " in tl:
                parts.append("Detected document type: beo")
            elif "receipt" in tl or "recibo" in tl:
                parts.append("Detected document type: receipt")
            elif "quote" in tl or "quotation" in tl or "orcamento" in tl or "orçamento" in tl:
                parts.append("Detected document type: quote")
        
        # Add the main document text
        parts.append("\n=== DOCUMENT TEXT ===")
        parts.append(text)
        
        # Add extraction instructions
        parts.append("\n=== INSTRUCTIONS ===")
        parts.append("Extract ALL relevant information from this document using semantic understanding, NOT keyword matching.")
        parts.append("Use your intelligence to identify:")
        parts.append("- Vendor/seller information (extract ALL fields regardless of labels - Empresa, Company, Vendor, etc.)")
        parts.append("- Buyer/customer information (extract ALL fields regardless of labels - Cliente, Customer, Ship To, etc.)")
        parts.append("- All dates, identifiers, contact information, financial values")
        parts.append("- Complete item extraction with quantities and prices")
        parts.append("- All totals, taxes, rates, discounts, and financial breakdowns")
        parts.append("- Use additionalProperties to capture any field that doesn't fit standard schema")
        parts.append("- Preserve original field names from document when possible (e.g., if document says 'Empresa', use 'Empresa' as field name)")
        parts.append("- Work in Portuguese, English, or mixed - understand semantic meaning, not literal words")
        parts.append("- Return a JSON object following the schema with all extracted information")
        
        return "\n".join(parts)

    def _load_system_prompt(self) -> str:
        """Use embedded system prompt to avoid blocking file I/O in request path."""
        return self._fallback_system_prompt()

    def _fallback_system_prompt(self) -> str:
        """Fallback system prompt if file loading fails."""
        return """You are a Commerce Document Extractor. Extract structured data from commercial documents and return JSON only.

Extract document type, buyer/vendor info, items with quantities and prices, totals, dates, and identify any risks or inconsistencies.

Return JSON following the canonical commerce document schema with proper data types and null values for missing fields."""

    def _load_json_schema(self) -> dict[str, Any]:
        """Load JSON schema for structured output.
        
        Schema is designed to be flexible and accept additional properties
        in buyer, vendor, shipping, dates, terms, items, totals, and meta
        to capture all relevant information from diverse document formats.
        """
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
                "buyer": {
                    "type": ["object", "null"],
                    "additionalProperties": True
                },
                "vendor": {
                    "type": ["object", "null"],
                    "additionalProperties": True
                },
                "event": {
                    "type": ["object", "null"],
                    "additionalProperties": True
                },
                "dates": {
                    "type": ["object", "null"],
                    "additionalProperties": True
                },
                "shipping": {
                    "type": ["object", "null"],
                    "additionalProperties": True
                },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": True,
                        "properties": {
                            "line_no": {"type": ["string", "integer", "null"]},
                            "sku": {"type": ["string", "null"]},
                            "name": {"type": ["string", "null"]},
                            "description": {"type": ["string", "null"]},
                            "qty": {"type": ["number", "null"]},
                            "unit": {"type": ["string", "null"]},
                            "unit_price": {"type": ["number", "null"]},
                            "taxes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": True
                                }
                            },
                            "line_total": {"type": ["number", "null"]}
                        }
                    }
                },
                "totals": {
                    "type": ["object", "null"],
                    "additionalProperties": True,
                    "properties": {
                        "subtotal": {"type": ["number", "null"]},
                        "discounts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": True
                            }
                        },
                        "taxes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": True
                            }
                        },
                        "freight": {"type": ["number", "null"]},
                        "other_charges": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": True
                            }
                        },
                        "grand_total": {"type": ["number", "null"]}
                    }
                },
                "terms": {
                    "type": ["object", "null"],
                    "additionalProperties": True,
                    "properties": {
                        "payment_terms": {"type": ["string", "null"]},
                        "installments": {"type": ["string", "null"]},
                        "notes": {"type": ["string", "null"]}
                    }
                },
                "signatures": {
                    "type": ["object", "null"],
                    "additionalProperties": True,
                    "properties": {
                        "customer_signed_at": {"type": ["string", "null"]},
                        "approver_signed_at": {"type": ["string", "null"]}
                    }
                },
                "risks": {"type": "array", "items": {"type": "string"}},
                "meta": {
                    "type": ["object", "null"],
                    "additionalProperties": True
                }
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
