"""
LLM routing classifier (context-first, allowlist-aware).

Overview
  Classifies a user message into one of the target agents (analytics,
  knowledge, commerce, triage) using an LLM with JSON Schema outputs and an
  optional ensemble. Falls back to deterministic heuristics when the backend
  is unavailable. Extracts allowlist tables/columns when present.

Design
  - Backend-agnostic via a small JSONLLMBackend protocol; default OpenAI client
    with JSON Schema formatting.
  - Optional ensemble (variants + scorer) with conservative confidence
    calibration. Strict decision validation to catch obvious misroutes.
  - Heuristic fallback prioritizes structured cues (allowlist/SQL‑like), then
    weak document phrasing signals, never relying solely on keywords.

Integration
  - Exposed via the `LLMClassifier.classify(...)` method; returns a
    `RouterDecision` (dataclass if available) or a plain mapping.
  - System/Examples prompts are loaded from `app/prompts/routing/` when present.

Usage
  >>> from app.routing.llm_classifier import LLMClassifier
  >>> dec = LLMClassifier().classify("quantos pedidos por mês?", allowlist={"orders": ["order_id"]})
  >>> dec.get("agent") in {"analytics", "knowledge", "commerce", "triage"}
  True
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping, Sequence
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

# Optional metrics
try:
    from app.infra.metrics import inc_counter as _inc_counter
except Exception:  # pragma: no cover - optional
    def _inc_counter(_name: str, labels: Mapping[str, str] | None = None, amount: float = 1.0) -> None:
        return


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
    """Backend using centralized LLM client with tool calling (preferred) or JSON Schema fallback."""

    def __init__(self, *, model: str, use_tool_calling: bool = True) -> None:
        from app.infra.llm_client import get_llm_client

        self._client = get_llm_client()
        if not self._client.is_available():
            raise RuntimeError("LLM client not available")
        self._default_model = model
        self._use_tool_calling = use_tool_calling

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

        # Prefer tool calling for token efficiency
        if self._use_tool_calling:
            try:
                return self._generate_with_tools(
                    system=system,
                    messages=messages,
                    json_schema=json_schema,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_output_tokens,
                )
            except Exception as exc:
                # Fallback to JSON Schema if tool calling fails
                self._log.warning("Tool calling failed, falling back to JSON Schema", extra={"error": str(exc)})

        # Fallback to JSON Schema
        return self._generate_with_json_schema(
            system=system,
            messages=messages,
            json_schema=json_schema,
            model=model_name,
            temperature=temperature,
            max_tokens=max_output_tokens,
        )

    def _generate_with_tools(
        self,
        *,
        system: str,
        messages: list[dict[str, str]],
        json_schema: Mapping[str, Any],
        model: str,
        temperature: float,
        max_tokens: int | None,
    ) -> Mapping[str, Any]:
        """Generate JSON using tool calling (more token-efficient)."""
        # Convert JSON schema to tool definition
        schema_name = str(json_schema.get("title", "RouterDecision"))[:32] or "RouterDecision"
        tool = {
            "type": "function",
            "function": {
                "name": schema_name,
                "description": json_schema.get("description", "Generate structured output"),
                "parameters": json_schema,
            },
        }

        resp = self._client.chat_completion_with_tools(
            messages=[{"role": "system", "content": system}, *messages],
            tools=[tool],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            tool_choice="required",
            max_retries=0,
        )

        if not resp or not resp.text:
            raise RuntimeError("tool calling returned empty response")

        # Parse tool call arguments as JSON
        data = self._client.extract_json(resp.text, schema=dict(json_schema))
        if data is None:
            raise RuntimeError("tool calling returned non-JSON content")
        return data

    def _generate_with_json_schema(
        self,
        *,
        system: str,
        messages: list[dict[str, str]],
        json_schema: Mapping[str, Any],
        model: str,
        temperature: float,
        max_tokens: int | None,
    ) -> Mapping[str, Any]:
        """Generate JSON using JSON Schema (fallback)."""
        resp = self._client.chat_completion(
            messages=[{"role": "system", "content": system}, *messages],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
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

    @property
    def _log(self):
        """Get logger for this backend."""
        try:
            from app.infra.logging import get_logger
            return get_logger(__name__)
        except Exception:
            import logging
            return logging.getLogger(__name__)


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
        enable_cache: bool = True,
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
        
        # Initialize routing cache
        self._cache = None
        if enable_cache:
            try:
                from app.infra.cache import RoutingCache
                self._cache = RoutingCache(ttl_seconds=3600, max_size=1000)
            except Exception as exc:
                self.log.warning("Routing cache unavailable", exc_info=exc)
                self._cache = None

    # Public API -------------------------------------------------------------
    def classify(
        self,
        message: str,
        allowlist: Mapping[str, Iterable[str]] | None = None,
        *,
        thread_id: str | None = None,
        locale: str = "pt-BR",
        rag_hits: int = 0,
        rag_min_score: float | None = None,
        has_attachment: bool = False,
        conversation_history: Sequence[dict[str, Any]] | None = None,
        last_answer: Mapping[str, Any] | None = None,
        relevant_context: Mapping[str, Any] | None = None,
    ) -> Any:
        """Return a RouterDecision (dataclass or plain dict) for *message*.

        When the backend is unavailable or errors, a deterministic heuristic
        decision is returned.
        """

        with start_span("routing.classify"):
            # Check cache first
            if self._cache:
                cached = self._cache.get(message, allowlist or {})
                if cached:
                    self.log.debug("Using cached routing decision")
                    cached["thread_id"] = thread_id
                    return self._return_final(cached)
            
            # Detect meta questions before LLM classification
            meta_type = self._detect_meta_question(message)
            if meta_type:
                decision = {
                    "agent": "triage",
                    "confidence": 1.0,
                    "reason": f"meta_question_{meta_type}",
                    "tables": [],
                    "columns": [],
                    "signals": ["meta_question", meta_type],
                    "thread_id": thread_id,
                }
                decision = self._apply_confidence_calibration(decision)
                if self._cache:
                    self._cache.set(message, allowlist or {}, decision)
                return self._return_final(decision)
            
            # Detect out-of-scope topics before LLM classification
            oos_topic = self._detect_out_of_scope(message)
            if oos_topic:
                decision = {
                    "agent": "triage",
                    "confidence": 1.0,
                    "reason": f"out_of_scope_{oos_topic}",
                    "tables": [],
                    "columns": [],
                    "signals": ["out_of_scope", oos_topic],
                    "thread_id": thread_id,
                }
                decision = self._apply_confidence_calibration(decision)
                if self._cache:
                    self._cache.set(message, allowlist or {}, decision)
                return self._return_final(decision)
            try:
                system = self._load_system_prompt(
                    allowlist or {},
                    rag_hits=rag_hits,
                    rag_min_score=rag_min_score,
                    has_attachment=has_attachment,
                    relevant_context=relevant_context
                )
                schema = _routerdecision_json_schema()
                if self._backend is None:
                    raise RuntimeError("no backend configured")

                # -------------------------------------------------------------
                # Ensemble routing (feature-flagged via env)
                # -------------------------------------------------------------
                import os as _os
                ensemble_enabled = str(_os.getenv("ROUTER_ENSEMBLE_ENABLED", "true")).strip().lower() in {"1","true","yes","on"}
                scorer_enabled = str(_os.getenv("ROUTER_SCORER_ENABLED", "true")).strip().lower() in {"1","true","yes","on"}

                if ensemble_enabled:
                    # Simplified ensemble: use evidence-based reasoning, not keyword filtering
                    # Load minimal examples for diversity, but rely primarily on evidence
                    ex_all = self._load_examples()
                    # Use only 1-2 examples per variant to reduce keyword dependency
                    minimal_neutral = ex_all[:2] if ex_all else []
                    
                    variants = [
                        ("neutral", minimal_neutral),
                        ("evidence_focused", minimal_neutral),  # Same examples, but system prompt emphasizes evidence
                    ]
                    votes: list[dict[str, Any]] = []
                    for tag, exs in variants:
                        messages = [*exs, {"role": "user", "content": message}]
                        try:
                            raw = self._backend.generate_json(
                                system=system,
                                messages=messages,
                                json_schema=schema,
                                model=self.model,
                                temperature=self.temperature,
                                max_output_tokens=self.max_output_tokens,
                            )
                            dec = _normalize_router_decision(raw, thread_id=thread_id)
                            if self._validate_decision(dec, message):
                                votes.append({"tag": tag, "decision": dec})
                            else:
                                self.log.info("ensemble: invalid LLM decision", extra={"tag": tag, "decision": dec})
                        except Exception as _e:
                            self.log.info("ensemble: variant failed", extra={"tag": tag, "reason": str(_e)})

                    # Majority voting
                    if votes:
                        from collections import Counter as _Counter
                        agent_counts = _Counter(v["decision"]["agent"] for v in votes)
                        top_agent, top_count = next(iter(agent_counts.most_common(1)))
                        # If clear majority, take the first decision for that agent
                        if top_count >= 2 or len(agent_counts) == 1:
                            chosen = next(v for v in votes if v["decision"]["agent"] == top_agent)["decision"]
                            chosen["signals"] = list({*chosen.get("signals", []), "ensemble_majority"})
                            # Apply optional confidence calibration
                            chosen = self._apply_confidence_calibration(chosen)
                            if self._cache:
                                self._cache.set(message, allowlist or {}, chosen)
                            return self._return_final(chosen)

                        # Tie-breaker using scorer
                        if scorer_enabled:
                            try:
                                scorer_dec = self._score_agents(message, candidates=[d["decision"] for d in votes])
                                scorer_dec["signals"] = list({*scorer_dec.get("signals", []), "ensemble_scorer"})
                                scorer_dec = self._apply_confidence_calibration(scorer_dec)
                                if self._cache:
                                    self._cache.set(message, allowlist or {}, scorer_dec)
                                return self._return_final(scorer_dec)
                            except Exception as _se:
                                # Conservative fallback: if no majority and scorer failed,
                                # drop to triage when confidence is low.
                                self.log.info("scorer failed; evaluating conservative fallback", extra={"reason": str(_se)})
                                # Read confidence_min from settings/env or use default
                                conf_min = 0.65
                                try:
                                    from app.config.settings import get_settings as _get_settings  # local import
                                    _cfg = _get_settings()
                                    conf_min = float(getattr(getattr(_cfg, "routing"), "confidence_min", conf_min))
                                except Exception:
                                    pass
                                # best observed confidence across votes (after calibration later as well)
                                try:
                                    best_conf = max(float(v["decision"].get("confidence", 0.0) or 0.0) for v in votes)
                                except Exception:
                                    best_conf = 0.0
                                if best_conf < (conf_min + 0.05):
                                    tri = {"agent": "triage", "confidence": max(best_conf, conf_min), "reason": "ensemble_tie_low_confidence", "tables": [], "columns": [], "signals": ["ensemble_tie", "low_confidence"], "thread_id": thread_id}
                                    tri = self._apply_confidence_calibration(tri)
                                    if self._cache:
                                        self._cache.set(message, allowlist or {}, tri)
                                    return self._return_final(tri)
                                # otherwise, return first but mark tie
                                first = dict(votes[0]["decision"])  # copy
                                first.setdefault("signals", []).append("ensemble_tie")
                                first = self._apply_confidence_calibration(first)
                                if self._cache:
                                    self._cache.set(message, allowlist or {}, first)
                                return self._return_final(first)

                    # If ensemble produced nothing valid, fall back to single-shot below

                # -------------------------------------------------------------
                # Single-shot LLM route (fallback)
                # Use minimal examples, focus on evidence-based reasoning
                # -------------------------------------------------------------
                # Load only 2-3 diverse examples for few-shot, not all
                examples = self._load_examples()
                # Use only 2 examples to avoid over-reliance on patterns
                minimal_examples = examples[:2] if examples else []
                messages = [*minimal_examples, {"role": "user", "content": message}]
                try:
                    raw = self._backend.generate_json(
                        system=system,
                        messages=messages,
                        json_schema=schema,
                        model=self.model,
                        temperature=self.temperature,
                        max_output_tokens=self.max_output_tokens,
                    )
                    decision = _normalize_router_decision(raw, thread_id=thread_id)
                    if self._validate_decision(decision, message):
                        decision = self._apply_confidence_calibration(decision)
                        if self._cache:
                            self._cache.set(message, allowlist or {}, decision)
                        return self._return_final(decision)
                    else:
                        self.log.info("LLM decision invalid, using heuristic", extra={"llm_decision": decision})
                        decision = self._heuristic_decide(message, allowlist or {}, thread_id=thread_id, locale=locale)
                        decision = self._apply_confidence_calibration(decision)
                        return self._return_final(decision)
                except Exception as llm_exc:
                    self.log.info("LLM failed, using heuristic", extra={"reason": str(llm_exc)})
                    decision = self._heuristic_decide(message, allowlist or {}, thread_id=thread_id, locale=locale)
                    decision = self._apply_confidence_calibration(decision)
                    if self._cache:
                        self._cache.set(message, allowlist or {}, decision)
                    return self._return_final(decision)
            except Exception as exc:
                self.log.info("classifier fallback engaged", extra={"reason": str(exc)})
                decision = self._heuristic_decide(
                    message, allowlist or {}, thread_id=thread_id, locale=locale
                )
            decision = self._apply_confidence_calibration(decision)
            if self._cache:
                self._cache.set(message, allowlist or {}, decision)
            return self._return_final(decision)

    # ---------------------------------------------------------------------
    # Scorer (tie-breaker)
    # ---------------------------------------------------------------------
    def _score_agents(self, message: str, *, candidates: list[dict[str, Any]]) -> dict[str, Any]:
        """Score candidate decisions using an LLM scorer prompt and return the best.

        The scorer receives the user message and candidate agent rationales and
        outputs normalized scores per agent. We pick the highest-scoring candidate.
        """
        if not candidates:
            raise ValueError("no candidates to score")
        try:
            import json as _json
            # Build compact scorer prompt
            summary = [{"agent": c.get("agent"), "reason": c.get("reason", "")} for c in candidates]
            scorer_system = (
                "You are a routing scorer. Given a user message and candidate agents with reasons, "
                "return JSON {\"scores\": {agent: float in [0,1], ...}} where scores sum is not required."
            )
            scorer_schema = {
                "type": "object",
                "properties": {"scores": {"type": "object", "additionalProperties": {"type": "number"}}},
                "required": ["scores"],
                "additionalProperties": False,
            }
            messages = [
                {"role": "user", "content": f"message: {message}\ncandidates: {_json.dumps(summary, ensure_ascii=False)}"}
            ]
            raw = self._backend.generate_json(
                system=scorer_system,
                messages=messages,
                json_schema=scorer_schema,
                model=self.model,
                temperature=self.temperature,
                max_output_tokens=256,
            )
            scores = dict(raw.get("scores", {}))
            # Choose candidate with max score; default to first if missing
            ranked = sorted(((scores.get(c.get("agent"), 0.0), idx) for idx, c in enumerate(candidates)), reverse=True)
            best_idx = ranked[0][1] if ranked else 0
            return candidates[best_idx]
        except Exception as e:
            # If scorer fails, return first candidate
            self.log.info("scorer exception", extra={"reason": str(e)})
            return candidates[0]

    # ---------------------------------------------------------------------
    # Confidence calibration
    # ---------------------------------------------------------------------
    def _apply_confidence_calibration(self, decision: dict[str, Any]) -> dict[str, Any]:
        """Apply simple piecewise calibration to decision["confidence"].

        Controlled by env `ROUTER_CALIBRATION` with JSON like:
        {"breaks": [0.3, 0.6, 0.85], "scales": [0.9, 1.0, 1.05, 1.0]}
        Fallback: conservative default that slightly boosts mid-range.
        """
        try:
            import os as _os, json as _json
            raw = _os.getenv("ROUTER_CALIBRATION")
            if raw:
                cfg = _json.loads(raw)
                breaks = list(cfg.get("breaks", []))
                scales = list(cfg.get("scales", []))
            else:
                breaks = [0.3, 0.6, 0.85]
                scales = [0.95, 1.00, 1.03, 1.00]
        except Exception:
            breaks = [0.3, 0.6, 0.85]
            scales = [0.95, 1.00, 1.03, 1.00]

        c = float(decision.get("confidence", 0.5) or 0.5)
        # find scale bucket
        idx = 0
        for b in breaks:
            if c > b:
                idx += 1
        s = scales[min(idx, len(scales) - 1)]
        calibrated = max(0.0, min(1.0, c * float(s)))
        out = dict(decision)
        out["confidence"] = calibrated
        return out

    def _detect_meta_question(self, query: str) -> str | None:
        """Detect if query is a meta question about system capabilities or usage.

        Parameters
        ----------
        query:
            User query text.

        Returns
        -------
        str | None
            Meta question type ("capabilities" or "usage") or None if not a meta question.
        """
        q = (query or "").lower().strip()
        if not q:
            return None

        capabilities_patterns = [
            r'^(quais|o que|what)\s+(são|sao|sua|suas|você|voce|voces|vocês)\s+(funcionalidade|capacidade|pode|consegue|faz)',
            r'^(quais|o que|what)\s+(você|voce|voces|vocês)\s+(pode|consegue|faz)',
            r'^(como|how)\s+(você|voce|voces|vocês|eu)\s+(pode|consegue|faço|fazer|uso|usar)',
            r'^(me\s+)?(mostre|mostra|explique|explica|diga|diz)\s+(o\s+)?(que|quais)\s+(você|voce|voces|vocês)\s+(pode|consegue|faz)',
            r'^(help|ajuda|ajude|socorro)',
        ]

        for pattern in capabilities_patterns:
            if re.search(pattern, q, re.IGNORECASE):
                return "capabilities"

        usage_patterns = [
            r'^(como|how)\s+(faço|fazer|uso|usar|consulto|consultar|busco|buscar)\s+(pedido|dados|informação|informacao|documento)',
            r'^(como|how)\s+(faço|fazer|uso|usar)\s+(para|pra)\s+(consultar|buscar|analisar|extrair)',
            r'^(como|how)\s+(consultar|buscar|analisar|extrair)\s+(pedido|dados|informação|informacao|documento)',
        ]

        for pattern in usage_patterns:
            if re.search(pattern, q, re.IGNORECASE):
                return "usage"

        return None

    def _detect_out_of_scope(self, query: str) -> str | None:
        """Detect if query is about topics outside system capabilities.
        
        Parameters
        ----------
        query:
            User query text.
            
        Returns
        -------
        str | None
            Out-of-scope topic type or None if query is in scope.
        """
        q = (query or "").lower().strip()
        if not q:
            return None
        
        weather = ("previsão do tempo", "previsao do tempo", "meteorologia", "clima", "tempo em ", "temperatura")
        news = ("notícias", "noticias", "news")
        markets = ("bolsa de valores", "ações", "dólar", "euro", "stock", "forex")
        code = ("programar em", "escreva um código", "write code")
        sports = ("futebol", "jogo", "basquete", "vôlei", "volei", "nba", "fifa", "champions", "copa do mundo")
        
        if any(k in q for k in weather):
            return "weather"
        if any(k in q for k in news):
            return "news"
        if any(k in q for k in markets):
            return "financial_markets"
        if any(k in q for k in code):
            return "code_generation"
        if any(k in q for k in sports):
            return "sports_entertainment"
        
        return None

    def _return_final(self, decision: dict[str, Any]) -> Any:
        """Record metrics and coerce the RouterDecision for return."""
        try:
            agent = str(decision.get("agent", "triage"))
            _inc_counter("router_decisions_total", {"agent": agent})
        except Exception:
            pass
        return _coerce_router_decision(decision)

    def _validate_decision(self, decision: dict, message: str) -> bool:
        """Validate if the LLM decision makes sense given the message."""
        agent = decision.get("agent", "")
        message_lower = message.lower()
        
        # CRITICAL RULES: Validate question type matches agent capability
        
        # Note: We don't do keyword-based validation here anymore.
        # The LLM should determine if the question is conceptual or data-driven.
        # This validation only checks for obvious contradictions that the LLM
        # should have caught (greetings, meta questions, etc.)
            
        # 2. Document processing MUST go to commerce
        doc_processing_verbs = ["processe", "analise", "extraia", "processar", "analisar", "extrair"]
        is_doc_processing = any(verb in message_lower for verb in doc_processing_verbs)
        if is_doc_processing and agent != "commerce":
            self.log.warning("LLM misclassified document processing", 
                           extra={"message": message, "agent": agent, "should_be": "commerce"})
            return False
            
        # 3. Greetings and meta questions MUST go to triage
        greeting_patterns = ["oi", "olá", "bom dia", "boa tarde", "boa noite", "tudo bem", "como está"]
        meta_patterns = ["o que você sabe", "o que você pode", "como você funciona", "o que você faz"]
        is_greeting = any(pattern in message_lower for pattern in greeting_patterns)
        is_meta = any(pattern in message_lower for pattern in meta_patterns)
        if (is_greeting or is_meta) and agent != "triage":
            self.log.warning("LLM misclassified greeting/meta question", 
                           extra={"message": message, "agent": agent, "should_be": "triage"})
            return False
            
        # 4. Definitions MUST go to knowledge
        definition_patterns = ["o que significa", "o que é", "what does", "what is", "definição", "significado"]
        is_definition = any(pattern in message_lower for pattern in definition_patterns)
        if is_definition and agent != "knowledge":
            self.log.warning("LLM misclassified definition", 
                           extra={"message": message, "agent": agent, "should_be": "knowledge"})
            return False
            
        # 5. Data queries SHOULD go to analytics
        data_query_patterns = ["quantos", "qual", "média", "soma", "total", "count", "average", "sum", "faturamento", "receita"]
        is_data_query = any(pattern in message_lower for pattern in data_query_patterns)
        if is_data_query and agent not in ["analytics", "knowledge"]:  # Allow knowledge for some data queries
            self.log.warning("LLM misclassified data query", 
                           extra={"message": message, "agent": agent, "should_be": "analytics"})
            return False
        
        # 6. Correlation/relationship analysis: Only route to analytics if explicitly asking for data
        # Questions about "relação" can be conceptual (knowledge) or data-driven (analytics)
        # Let LLM decide based on question type, don't force analytics
            
        # Check for meta questions (should go to triage)
        meta_patterns = ["o que você sabe", "o que você pode", "como você funciona", "o que você faz"]
        is_meta = any(pattern in message_lower for pattern in meta_patterns)
        if is_meta and agent != "triage":
            self.log.warning("LLM misclassified meta question", 
                           extra={"message": message, "agent": agent, "should_be": "triage"})
            return False
            
        return True

    # Internals --------------------------------------------------------------
    def _load_system_prompt(
        self, 
        allowlist: Mapping[str, Iterable[str]], 
        rag_hits: int = 0,
        rag_min_score: float | None = None,
        has_attachment: bool = False,
        relevant_context: Mapping[str, Any] | None = None
    ) -> str:
        # Try to load from prompts file; fallback to embedded minimal prompt
        try:
            base_dir = self.base_dir.parent / "prompts" / "routing"
            system_path = base_dir / "system.txt"
            if system_path.exists():
                content = system_path.read_text(encoding="utf-8")
            else:
                content = (
                    "You are a router. Classify the user's message into one of: analytics, knowledge, commerce, triage. "
                    "Also extract any tables/columns present in the message according to the provided allowlist."
                )
        except Exception:
            content = (
                "You are a router. Classify the user's message into one of: analytics, knowledge, commerce, triage. "
                "Also extract any tables/columns present in the message according to the provided allowlist."
            )
        
        # Inject evidence-based context
        allowlist_json = _allowlist_to_json(allowlist)
        has_allowlist = bool(allowlist and any(allowlist.values()))
        
        evidence_context = f"""
## CURRENT EVIDENCE (Use this to decide routing)

ALLOWLIST: {allowlist_json}
- Has allowlist: {has_allowlist}
- Available tables: {len(allowlist) if allowlist else 0}

RAG EVIDENCE:
- RAG hits: {rag_hits} (0 = no relevant documents found)
- RAG min score: {rag_min_score if rag_min_score is not None else 'N/A'}

ATTACHMENT EVIDENCE:
- Has attachment: {has_attachment}

**IMPORTANT**: Only route to an agent if the required evidence is available.
- Analytics requires allowlist tables/columns
- Knowledge requires RAG hits > 0
- Commerce requires file attachment
"""
        
        # Add conversation context if available and relevant
        context_section = ""
        if relevant_context and relevant_context.get("is_relevant", False):
            context_summary = relevant_context.get("context_summary", "")
            context_section = f"""

## CONVERSATION CONTEXT (Validated as Relevant)

{context_summary}

**IMPORTANTE**: Este contexto foi validado como relevante para a query atual.
Use este contexto para entender referências a mensagens anteriores e manter continuidade.
Se a query claramente inicia um novo tópico, ignore este contexto e route normalmente.
"""
        elif relevant_context and not relevant_context.get("is_relevant", False):
            context_section = """

## CONVERSATION CONTEXT (Not Relevant - New Topic Detected)

**IMPORTANTE**: A query atual representa uma mudança de tópico ou não está
relacionada ao histórico recente. Processe esta query isoladamente, sem
considerar contexto anterior. Route baseado apenas na query atual.
"""
        
        injected = content + "\nALLOWLIST_JSON=" + allowlist_json + evidence_context + context_section
        return injected

    def _load_examples(self) -> list[dict[str, str]]:
        # Load few-shot examples if available
        try:
            base_dir = self.base_dir.parent / "prompts" / "routing"
            examples_path = base_dir / "examples.jsonl"
            if not examples_path.exists():
                return []
            rows: list[dict[str, str]] = []
            for line in examples_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                import json as _json
                obj = _json.loads(line)
                # Expect keys: role/content or input/output; adapt minimally
                if "role" in obj and "content" in obj:
                    rows.append({"role": str(obj["role"]), "content": str(obj["content"])})
                elif "input" in obj:
                    rows.append({"role": "user", "content": str(obj["input"])})
                    if "output" in obj:
                        rows.append({"role": "assistant", "content": str(obj["output"])})
            return rows
        except Exception:
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
        # Tuned weights to reduce over-routing to analytics when signals are weak
        # Check for definition questions first
        definition_keywords = ["o que significa", "o que é", "what does", "what is", "definição", "significado"]
        is_definition = any(keyword in norm for keyword in definition_keywords)
        
        # Check for greetings
        greeting_patterns = ["oi", "olá", "bom dia", "boa tarde", "boa noite", "tudo bem", "como está", "hello", "hi", "good morning"]
        is_greeting = any(pattern in norm for pattern in greeting_patterns)
        
        # Check for data queries (should go to analytics)
        data_query_patterns = ["quantos", "qual", "média", "soma", "total", "count", "average", "sum", "faturamento", "receita", "temos"]
        is_data_query = any(pattern in norm for pattern in data_query_patterns)
        
        # Check for explicit data request signals (must have these to be data-driven)
        explicit_data_signals = ["nos nossos dados", "no banco", "calcular", "calcule", "média", "quantos", "qual o valor", "nos pedidos", "em nossos dados"]
        has_explicit_data_request = any(signal in norm for signal in explicit_data_signals)
        
        # Check for correlation/relationship WITHOUT explicit data request → conceptual
        correlation_patterns = ["relação entre", "correlação", "como afeta", "impacto de", "impacto sobre", "efeito de", "relação com"]
        has_correlation_phrase = any(pattern in norm for pattern in correlation_patterns)
        # If has correlation phrase but NO explicit data request → treat as conceptual
        is_correlation_conceptual = has_correlation_phrase and not has_explicit_data_request
        
        # Check for commerce document processing (REACT: Reasoning + Acting)
        doc_processing_verbs = ["processe", "analise", "extraia", "processar", "analisar", "extrair", "review", "process", "analyze", "extract"]
        is_doc_processing = any(verb in norm for verb in doc_processing_verbs)
        
        # REACT: Additional reasoning for document processing
        # Check for document types even without explicit verbs
        doc_types = ["fatura", "nota fiscal", "contrato", "pedido", "documento", "invoice", "contract", "order", "document", "catering", "fornecimento"]
        has_doc_types = any(doc_type in norm for doc_type in doc_types)
        
        # REACT: Combine verb + document type for stronger signal
        is_doc_processing = is_doc_processing or (has_doc_types and any(word in norm for word in ["dados", "data", "informações", "information"]))
        
        # Check for conceptual questions (should go to knowledge, not commerce)
        conceptual_questions = ["como começar", "como funciona", "o que é", "estratégias", "marketing", "como fazer", "melhores práticas", "como escolher"]
        is_conceptual = any(concept in norm for concept in conceptual_questions)
        
        # Check for meta questions (should go to triage)
        meta_questions = ["o que você sabe", "o que você pode", "como você funciona", "o que você faz"]
        is_meta = any(meta in norm for meta in meta_questions)
        
        # ENHANCED HEURISTIC: More specific pattern matching
        if is_definition:
            scores = {
                "analytics": 0.0,  # Force knowledge for definitions
                "commerce": 0.0,   # CONSTRAINT: No commerce for definitions
                "knowledge": 0.95, # High score for definitions
                "triage": 0.0,     # CONSTRAINT: No triage for definitions
            }
        elif is_correlation_conceptual:
            # Questions about relationships WITHOUT explicit data request → Conceptual → Knowledge
            scores = {
                "analytics": 0.0,  # NOT analytics if conceptual
                "commerce": 0.0,   # CONSTRAINT: No commerce
                "knowledge": 0.95, # High score for conceptual relationship questions
                "triage": 0.0,     # CONSTRAINT: No triage
            }
        elif is_data_query or (has_correlation_phrase and has_explicit_data_request):
            # Only route to analytics if explicit data request signals present
            scores = {
                "analytics": 0.98, # High score for explicit data queries
                "commerce": 0.0,   # CONSTRAINT: No commerce for data queries
                "knowledge": 0.0,  # CONSTRAINT: No knowledge for explicit data queries
                "triage": 0.0,     # CONSTRAINT: No triage for data queries
            }
        elif is_greeting or is_meta:
            scores = {
                "analytics": 0.0,  # Force triage for greetings and meta questions
                "commerce": 0.0,
                "knowledge": 0.0,
                "triage": 0.95,  # High score for greetings and meta questions
            }
        elif is_conceptual:
            # CONSTRAINT SATISFACTION: Conceptual questions MUST go to knowledge
            # This is the critical fix for "Como começar um e-commerce?" cases
            scores = {
                "analytics": 0.0,  # CONSTRAINT: No analytics for conceptual questions
                "commerce": 0.0,   # CONSTRAINT: No commerce for conceptual questions
                "knowledge": 0.98, # CONSTRAINT: Very high score for conceptual questions
                "triage": 0.0,     # CONSTRAINT: No triage for conceptual questions
            }
        elif is_doc_processing:
            # CONSTRAINT SATISFACTION: Document processing MUST go to commerce
            scores = {
                "analytics": 0.0,  # CONSTRAINT: No analytics for document processing
                "commerce": 0.98,  # CONSTRAINT: Very high score for document processing
                "knowledge": 0.0,  # CONSTRAINT: No knowledge for document processing
                "triage": 0.0,     # CONSTRAINT: No triage for document processing
            }
        else:
            # Default scoring for ambiguous cases
            scores = {
                "analytics": min(1.0, 0.8 * allowlist_score + 0.6 * sqlish_score),
                "commerce": min(1.0, 0.9 * commerce_score),
                "knowledge": min(1.0, 1.0 * knowledge_score),
                "triage": 0.3,  # Default triage score for ambiguous cases
            }
        # ENSEMBLE DECISION MAKING: Combine multiple decision factors
        agent, best = max(scores.items(), key=lambda kv: kv[1])
        
        # ENSEMBLE: Additional validation layer
        # Check if the decision makes sense given the context
        decision_makes_sense = True
        
        # Validate commerce decisions
        if agent == "commerce" and not is_doc_processing and not has_doc_types:
            decision_makes_sense = False
            
        # Validate analytics decisions  
        if agent == "analytics" and is_definition:
            decision_makes_sense = False
            
        # Validate triage decisions
        if agent == "triage" and (is_doc_processing or is_definition):
            decision_makes_sense = False
            
        # ENSEMBLE: Override if decision doesn't make sense
        if not decision_makes_sense:
            if is_doc_processing:
                agent = "commerce"
                best = 0.95
            elif is_definition:
                agent = "knowledge" 
                best = 0.95
            elif is_conceptual:
                agent = "knowledge"
                best = 0.95
            elif is_greeting:
                agent = "triage"
                best = 0.95

        # Confidence: base 0.5 + scaled best score; fall back to triage if weak.
        if best < 0.35:
            agent = "triage"
            confidence = 0.35
            reason = "fallback: low structured signals"
        else:
            confidence = min(0.92, 0.48 + 0.42 * best)
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
