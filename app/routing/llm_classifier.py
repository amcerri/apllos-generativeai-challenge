"""
Routing LLM classifier

Overview
--------
Classifies a user message into one of the assistant agents (analytics,
knowledge, commerce, triage) and extracts table/column hints using a
language model with Structured Outputs. Falls back to a lightweight
heuristic classifier when the LLM client is unavailable.

Design
------
- Prompts live in `app/prompts/routing/{system.txt,examples.jsonl}`.
- Allowlist (tables → columns) is injected into the system prompt by
  replacing the `<<<ALLOWLIST_JSON>>>` placeholder.
- Pluggable LLM backend with an optional OpenAI implementation using
  JSON Schema (strict) response formatting.
- Output normalized to the `RouterDecision` contract (dict or dataclass).

Integration
-----------
- Import and call `classify(message, allowlist, thread_id=None)`.
- Provide an LLM backend (see `OpenAIJSONBackend`) or rely on the fallback
  rules for basic routing in constrained environments.

Usage
-----
>>> from app.routing.llm_classifier import LLMClassifier, OpenAIJSONBackend
>>> clf = LLMClassifier()  # will try OpenAI if available, else fallback
>>> decision = clf.classify("Qual foi a receita por mês em 2017?", {
...     "orders": ["order_id", "order_purchase_timestamp", "order_status"],
...     "order_items": ["order_id", "price", "freight_value"],
... })
>>> isinstance(decision, dict) or getattr(decision, "agent", None) in {"analytics","knowledge","commerce","triage"}
True
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

try:  # Optional: logging
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


start_span: Any

try:  # Optional: tracing helpers
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attributes: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span


# Optional: RouterDecision dataclass
ROUTER_DECISION_CLS: Any
try:
    from app.contracts.router_decision import RouterDecision as _RouterDecision

    ROUTER_DECISION_CLS = _RouterDecision
except Exception:  # pragma: no cover - optional
    ROUTER_DECISION_CLS = None


__all__ = [
    "LLMClassifier",
    "OpenAIJSONBackend",
]


# ---------------------------------------------------------------------------
# Backends
# ---------------------------------------------------------------------------
@runtime_checkable
class JSONLLMBackend(Protocol):
    """Protocol for backends that generate JSON matching a provided schema."""

    def generate_json(
        self,
        *,
        system: str,
        messages: list[dict[str, str]],
        json_schema: Mapping[str, Any],
        model: str | None = None,
        temperature: float = 0.0,
        max_output_tokens: int | None = None,
    ) -> Mapping[str, Any]: ...


class OpenAIJSONBackend:
    """Backend using centralized LLM client with JSON Schema response formatting."""

    def __init__(self, *, model: str) -> None:
        from app.infra.llm_client import get_llm_client

        self._client = get_llm_client()
        if not self._client.is_available():
            raise RuntimeError("LLM client not available")
        self._default_model = model

    def generate_json(
        self,
        *,
        system: str,
        messages: list[dict[str, str]],
        json_schema: Mapping[str, Any],
        model: str | None = None,
        temperature: float = 0.0,
        max_output_tokens: int | None = None,
    ) -> Mapping[str, Any]:
        model_name = model or self._default_model
        resp = self._client.chat_completion(
            messages=[{"role": "system", "content": system}, *messages],
            model=model_name,
            temperature=temperature,
            max_tokens=max_output_tokens,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": str(json_schema.get("title", "RouterDecision"))[:32] or "RouterDecision",
                    "schema": json_schema,
                    "strict": True,
                },
            },
            max_retries=0,
        )
        content = (resp.text if resp else "").strip()
        data = self._client.extract_json(content, schema=dict(json_schema))
        if data is None:
            raise RuntimeError("backend returned non-JSON content")
        return data


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------
class LLMClassifier:
    """LLM-powered router with allowlist-aware extraction and safe fallback.

    If no backend is provided, attempts to create an OpenAI backend; if that
    fails, classification falls back to simple heuristics.
    """

    def __init__(
        self,
        *,
        backend: JSONLLMBackend | None = None,
        model: str | None = None,
        temperature: float = 0.0,
        max_output_tokens: int | None = 512,
        base_dir: Path | None = None,
    ) -> None:
        self.log = get_logger(__name__)
        self.temperature = float(temperature)
        # Resolve model from settings if not provided
        if model is None:
            try:
                from app.config.settings import get_settings as _get_settings
                _cfg = _get_settings()
                model = _cfg.models.router.name
            except Exception:
                model = "gpt-4o-mini"
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent
        self._backend = backend
        if self._backend is None:
            try:
                self._backend = OpenAIJSONBackend(model=self.model)
            except Exception as exc:  # pragma: no cover - optional
                self.log.warning(
                    "LLM backend unavailable; falling back to heuristics", exc_info=exc
                )
                self._backend = None

    # Public API -------------------------------------------------------------
    def classify(
        self,
        message: str,
        allowlist: Mapping[str, Iterable[str]] | None = None,
        *,
        thread_id: str | None = None,
        locale: str = "pt-BR",
    ) -> Any:
        """Return a RouterDecision (dataclass or plain dict) for *message*.

        When the backend is unavailable or errors, a deterministic heuristic
        decision is returned.
        """

        with start_span("routing.classify"):
            try:
                system = self._load_system_prompt(allowlist or {})
                examples = self._load_examples()
                messages = [
                    *examples,
                    {"role": "user", "content": message},
                ]
                schema = _routerdecision_json_schema()
                if self._backend is None:
                    raise RuntimeError("no backend configured")
                raw = self._backend.generate_json(
                    system=system,
                    messages=messages,
                    json_schema=schema,
                    model=self.model,
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                )
                decision = _normalize_router_decision(raw, thread_id=thread_id)
                return _coerce_router_decision(decision)
            except Exception as exc:
                self.log.info("classifier fallback engaged", extra={"reason": str(exc)})
                decision = self._heuristic_decide(
                    message, allowlist or {}, thread_id=thread_id, locale=locale
                )
                return _coerce_router_decision(decision)

    # Internals --------------------------------------------------------------
    def _load_system_prompt(self, allowlist: Mapping[str, Iterable[str]]) -> str:
        # Embedded minimal system prompt to avoid blocking IO in ASGI path
        base = (
            "You are a router. Classify the user's message into one of: analytics, knowledge, commerce, triage. "
            "Also extract any tables/columns present in the message according to the provided allowlist."
        )
        injected = base + "\nALLOWLIST_JSON=" + _allowlist_to_json(allowlist)
        return injected

    def _load_examples(self) -> list[dict[str, str]]:
        # Skip disk reads; keep examples empty for fast routing
        return []

    def _heuristic_decide(
        self,
        message: str,
        allowlist: Mapping[str, Iterable[str]],
        *,
        thread_id: str | None,
        locale: str,
    ) -> dict[str, Any]:
        """
        Context-first deterministic fallback used only when the LLM backend
        is unavailable or fails. This does **not** try to outsmart the LLM; it
        derives intent from structured cues, prioritizing allowlist overlap and
        SQL-like structure. Keyword hints are used only as weak assistance.

        Heuristic signals (ordered by weight)
        -------------------------------------
        - Allowlist overlap (tables/columns) → strong signal for 'analytics'.
        - SQL-ish structure (SELECT ... FROM, ```sql fences) → medium signal for 'analytics'.
        - Commerce document structure cues (currency + totals-like terms) → medium for 'commerce'.
        - Document-style phrasing indicating policy/how-to with no tabular cues → weak for 'knowledge'.
        """
        text = (message or "")
        norm = text.lower()

        # ---- Strong signal: allowlist overlap (context-first) ----------------
        words = set(re.findall(r"[a-zA-Z0-9_]+", norm))
        hit_tables: set[str] = set()
        hit_columns: set[str] = set()
        for t, cols in allowlist.items():
            t_norm = str(t).strip().lower()
            if t_norm and t_norm in words:
                hit_tables.add(str(t))
            for c in cols:
                c_norm = str(c).strip().lower()
                if c_norm and c_norm in words:
                    hit_columns.add(str(c))

        allowlist_score = min(1.0, 0.6 * len(hit_tables) + 0.3 * len(hit_columns))

        # ---- Medium signal: SQL-like structure (structure, not keywords) -----
        has_sql_block = "```sql" in norm or norm.strip().startswith("select ")
        has_select_from = bool(re.search(r"\bselect\b.+\bfrom\b", norm, flags=re.S))
        sqlish_score = 0.5 if has_sql_block else (0.4 if has_select_from else 0.0)

        # ---- Commerce cues (structural-ish): currency + totals-like markers --
        has_currency = bool(re.search(r"(?:r\$|\$|usd|brl|eur)\s*\d", norm))
        has_total_terms = bool(re.search(r"\b(total|subtotal|tax|imposto|valor)\b", norm))
        commerce_score = 0.5 if (has_currency and has_total_terms) else 0.0

        # ---- Knowledge cues (weak): procedural/policy phrasing sans tables ---
        # Keep this weak to avoid overshadowing analytics when allowlist hits exist.
        knowledge_phrasing = bool(
            re.search(r"\b(como|passo a passo|pol[ií]tica|manual|documenta[cç][aã]o)\b", norm)
        )
        knowledge_score = 0.3 if (knowledge_phrasing and not hit_tables and not hit_columns) else 0.0

        # Aggregate per-agent scores (bounded in [0,1])
        scores = {
            "analytics": min(1.0, allowlist_score + sqlish_score),
            "commerce": min(1.0, commerce_score),
            "knowledge": min(1.0, knowledge_score),
        }
        agent, best = max(scores.items(), key=lambda kv: kv[1])

        # Confidence: base 0.5 + scaled best score; fall back to triage if weak.
        if best < 0.35:
            agent = "triage"
            confidence = 0.35
            reason = "fallback: low structured signals"
        else:
            confidence = min(0.9, 0.5 + 0.4 * best)
            if agent == "analytics":
                reason = "allowlist/SQL structure indicates tabular intent"
            elif agent == "commerce":
                reason = "amounts and totals-like structure indicate commercial document"
            else:
                reason = "procedural/document intent without tabular cues"

        # Build signals for observability (no hard keyword dependence)
        signals: list[str] = []
        if hit_tables:
            signals.append(f"allowlist_tables:{len(hit_tables)}")
        if hit_columns:
            signals.append(f"allowlist_columns:{len(hit_columns)}")
        if has_sql_block or has_select_from:
            signals.append("sql_like")
        if has_currency and has_total_terms:
            signals.append("commerce_amounts")
        if knowledge_phrasing and not (hit_tables or hit_columns):
            signals.append("doc_style")

        return {
            "agent": agent,
            "confidence": float(confidence),
            "reason": reason,
            "tables": sorted(hit_tables),
            "columns": sorted(hit_columns),
            "signals": signals,
            "thread_id": thread_id,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _allowlist_to_json(mapping: Mapping[str, Iterable[str]]) -> str:
    norm: dict[str, list[str]] = {}
    for t, cols in mapping.items():
        t2 = str(t).strip()
        if not t2:
            continue
        cols2 = sorted({str(c).strip() for c in cols if str(c).strip()})
        norm[t2] = cols2
    return json.dumps(norm, ensure_ascii=False, sort_keys=True)


def _routerdecision_json_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "RouterDecision",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "agent": {"type": "string", "enum": ["analytics", "knowledge", "commerce", "triage"]},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "reason": {"type": "string", "minLength": 1, "maxLength": 200},
            "tables": {"type": "array", "items": {"type": "string"}},
            "columns": {"type": "array", "items": {"type": "string"}},
            "signals": {"type": "array", "items": {"type": "string"}},
            "thread_id": {"type": ["string", "null"]},
        },
        "required": ["agent", "confidence", "reason", "tables", "columns", "signals", "thread_id"],
    }


def _normalize_router_decision(obj: Mapping[str, Any], *, thread_id: str | None) -> dict[str, Any]:
    agent = str(obj.get("agent", "triage"))
    if agent not in {"analytics", "knowledge", "commerce", "triage"}:
        agent = "triage"
    try:
        confidence = float(obj.get("confidence", 0.5))
    except Exception:
        confidence = 0.5
    reason = str(obj.get("reason", "router fallback"))[:200]

    def _as_list(v: Any) -> list[str]:
        if isinstance(v, list):
            return [str(x) for x in v if isinstance(x, str | int | float)]
        return []

    tables = _as_list(obj.get("tables"))
    columns = _as_list(obj.get("columns"))
    signals = _as_list(obj.get("signals"))
    return {
        "agent": agent,
        "confidence": max(0.0, min(1.0, confidence)),
        "reason": reason,
        "tables": tables,
        "columns": columns,
        "signals": signals,
        "thread_id": obj.get("thread_id", thread_id),
    }


def _coerce_router_decision(dec: Mapping[str, Any]) -> Any:
    """Return a RouterDecision dataclass when available; else a plain dict."""

    if ROUTER_DECISION_CLS is None:
        return dict(dec)
    # Try common constructors
    try:
        if hasattr(ROUTER_DECISION_CLS, "from_dict"):
            return ROUTER_DECISION_CLS.from_dict(dec)
        if hasattr(ROUTER_DECISION_CLS, "from_mapping"):
            return ROUTER_DECISION_CLS.from_mapping(dec)
        return ROUTER_DECISION_CLS(**dec)
    except Exception:
        return dict(dec)
