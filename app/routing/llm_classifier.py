"""
Routing LLM classifier

Overview
    Classifies a user message into one of the assistant agents (analytics,
    knowledge, commerce, triage) and extracts table/column hints using a
    language model with Structured Outputs. Falls back to a lightweight
    heuristic classifier when the LLM client is unavailable.

Design
    - Prompts live in `app/prompts/routing/{system.txt,examples.jsonl}`.
    - Allowlist (tables → columns) is injected into the system prompt by
      replacing the `<<<ALLOWLIST_JSON>>>` placeholder.
    - Pluggable LLM backend with an optional OpenAI implementation using
      JSON Schema (strict) response formatting.
    - Output normalized to the `RouterDecision` contract (dict or dataclass).

Integration
    - Import and call `classify(message, allowlist, thread_id=None)`.
    - Provide an LLM backend (see `OpenAIJSONBackend`) or rely on the fallback
      rules for basic routing in constrained environments.

Usage
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
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

try:  # Optional: structlog logger
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
    """Minimal OpenAI backend using strict JSON Schema response formatting.

    Requires the `openai` SDK (>= 1.0). If the package or credentials are not
    available, construction will raise and the caller should handle fallback.
    """

    def __init__(self, *, model: str = "gpt-4.1-mini") -> None:
        try:
            from openai import OpenAI
        except Exception as exc:  # pragma: no cover - optional path
            raise RuntimeError("openai SDK not available") from exc
        self._client = OpenAI()
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

        response = self._client.chat.completions.create(
            model=model_name,
            temperature=temperature,
            messages=[{"role": "system", "content": system}, *messages],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": str(json_schema.get("title", "RouterDecision"))[:32]
                    or "RouterDecision",
                    "schema": json_schema,
                    "strict": True,
                },
            },
            max_tokens=max_output_tokens,
        )
        # Extract JSON content (single choice expected)
        content = (response.choices[0].message.content or "").strip()
        try:
            return json.loads(content)
        except Exception as exc:
            raise RuntimeError("backend returned non-JSON content") from exc


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
        model: str = "gpt-4.1-mini",
        temperature: float = 0.0,
        max_output_tokens: int | None = 512,
        base_dir: Path | None = None,
    ) -> None:
        self.log = get_logger(__name__)
        self.temperature = float(temperature)
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent
        self._backend = backend
        if self._backend is None:
            try:
                self._backend = OpenAIJSONBackend(model=model)
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
        sys_path = self.base_dir / "prompts" / "routing" / "system.txt"
        text = sys_path.read_text(encoding="utf-8")
        injected = text.replace("<<<ALLOWLIST_JSON>>>", _allowlist_to_json(allowlist))
        return injected

    def _load_examples(self) -> list[dict[str, str]]:
        ex_path = self.base_dir / "prompts" / "routing" / "examples.jsonl"
        if not ex_path.exists():  # pragma: no cover - optional
            return []
        out: list[dict[str, str]] = []
        for line in ex_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            inp = str(obj.get("input", ""))
            outp = obj.get("output", {})
            if inp and isinstance(outp, Mapping):
                out.append({"role": "user", "content": inp})
                out.append({"role": "assistant", "content": json.dumps(outp, ensure_ascii=False)})
        return out

    def _heuristic_decide(
        self,
        message: str,
        allowlist: Mapping[str, Iterable[str]],
        *,
        thread_id: str | None,
        locale: str,
    ) -> dict[str, Any]:
        msg = (message or "").strip()
        msg_l = msg.lower()
        # Signals
        signals: set[str] = set()
        if any(
            tok in msg_l
            for tok in (
                ".pdf",
                ".doc",
                ".docx",
                "invoice",
                "nfe",
                "nota fiscal",
                "beo",
                "purchase order",
                "order form",
                "contrato",
                "proposta",
                "orçamento",
                "romaneio",
            )
        ):
            signals.add("commerce_doc")
        if any(
            tok in msg_l
            for tok in ("select", "from", "where", "group by", "order by", "limit", "join")
        ):
            signals.add("sql_intent")
        if any(
            tok in msg_l
            for tok in (
                "manual",
                "política",
                "policy",
                "docs",
                "documento",
                "RAG",
                "segundo o documento",
            )
        ):
            signals.add("doc_intent")
        if locale.lower().startswith("pt"):
            signals.add("language_ptbr")

        # Extract tables/columns from allowlist by word matching
        words = {w.strip(".,:;()[]{}\"'`").lower() for w in msg.split()}
        tables: list[str] = []
        columns: list[str] = []
        for t, cols in allowlist.items():
            if t.lower() in words:
                tables.append(t)
                signals.add("mentions_table")
            for c in cols:
                if c.lower() in words:
                    columns.append(c)
                    signals.add("mentions_column")
        # Decide agent
        agent = "triage"
        conf = 0.35
        reason = "ambiguous intent"
        if "commerce_doc" in signals:
            agent, conf, reason = "commerce", 0.82, "document cues (invoice/PO/etc.)"
        elif "sql_intent" in signals or tables or columns:
            agent, conf, reason = "analytics", 0.72, "tabular cues and/or SQL intent"
        elif "doc_intent" in signals:
            agent, conf, reason = "knowledge", 0.65, "procedural/policy document intent"

        return {
            "agent": agent,
            "confidence": max(0.0, min(1.0, float(conf))),
            "reason": reason,
            "tables": sorted(set(tables)),
            "columns": sorted(set(columns)),
            "signals": sorted(signals),
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
        "required": ["agent", "confidence", "reason", "tables", "columns", "signals"],
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
