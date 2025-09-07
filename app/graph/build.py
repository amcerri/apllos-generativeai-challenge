"""
Graph builder (LangGraph wiring for multi‑agent assistant).

Overview
--------
Assemble a LangGraph graph that routes user requests across four specialized
agents (analytics, knowledge, commerce, triage) using a context‑first
supervisor. The build is dependency‑light and degrades gracefully if LangGraph
is not available, returning a descriptive stub for tests.

Design
------
- Optional imports for LangGraph; provide safe fallbacks.
- Nodes wrap our agent components with minimal, business‑centric I/O.
- Routing: LLM classifier → deterministic supervisor with single‑pass fallbacks.
- Human‑in‑the‑loop: optional SQL approval gate emitted before execution.
- Checkpointing: integrated when available via the infra helper.

Integration
-----------
- Use this builder from the API layer or from `assistant.py` to obtain a
  compiled graph. Example usage below works with or without LangGraph installed.

Usage
-----
>>> from app.graph.build import build_graph
>>> g = build_graph(require_sql_approval=False)
>>> bool(g)  # a compiled graph or a descriptive stub
True
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

# ---------------------------------------------------------------------------
# Optional dependencies and infra fallbacks
# ---------------------------------------------------------------------------
END: Any
StateGraph: Any
try:  # LangGraph (optional at import time)
    from langgraph.graph import END as _END
    from langgraph.graph import StateGraph as _StateGraph

    END, StateGraph = _END, _StateGraph
except Exception:  # pragma: no cover - optional
    END, StateGraph = "__END__", None

try:  # Logging
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - simple fallback
        return _logging.getLogger(component)


# Tracing (single alias)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: Mapping[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

get_checkpointer: Any
try:
    from app.infra.checkpointer import get_checkpointer as _get_checkpointer

    get_checkpointer = _get_checkpointer
except Exception:  # pragma: no cover - optional
    get_checkpointer = None

# Human gates
make_sql_gate: Any
try:
    from app.graph.interrupts import make_sql_gate as _make_sql_gate

    make_sql_gate = _make_sql_gate
except Exception:  # pragma: no cover - optional

    def make_sql_gate(
        *,
        sql: str,
        params: Mapping[str, Any] | None = None,
        limit: int | None = None,
        tables: Sequence[str] | None = None,
        reason: str = "Confirmar execução de SQL",
    ) -> dict[str, Any]:
        return {
            "type": "human_interrupt",
            "name": "sql_execution",
            "details": {
                "sql": sql,
                "params": dict(params or {}),
                "limit": limit,
                "tables": list(tables or []),
            },
        }


# Router & Supervisor
LLMClassifier: Any
try:
    from app.routing.llm_classifier import LLMClassifier as _LLMClassifier

    LLMClassifier = _LLMClassifier
except Exception:  # pragma: no cover - optional
    LLMClassifier = None

apply_routing_rules: Any
try:
    import app.routing.supervisor as _supervisor

    apply_routing_rules = getattr(_supervisor, "apply_routing_rules", None)
    if apply_routing_rules is None:

        def apply_routing_rules(
            decision: Mapping[str, Any], *, allowlist: Mapping[str, list[str]] | None = None
        ) -> Mapping[str, Any]:
            return decision

except Exception:  # pragma: no cover - optional

    def apply_routing_rules(
        decision: Mapping[str, Any], *, allowlist: Mapping[str, list[str]] | None = None
    ) -> Mapping[str, Any]:
        return decision


# Agents: analytics
AnalyticsPlanner: Any
try:
    from app.agents.analytics.planner import AnalyticsPlanner as _AnalyticsPlanner

    AnalyticsPlanner = _AnalyticsPlanner
except Exception:
    AnalyticsPlanner = None

AnalyticsExecutor: Any
try:
    from app.agents.analytics.executor import AnalyticsExecutor as _AnalyticsExecutor

    AnalyticsExecutor = _AnalyticsExecutor
except Exception:
    AnalyticsExecutor = None

AnalyticsNormalizer: Any
try:
    from app.agents.analytics.normalize import AnalyticsNormalizer as _AnalyticsNormalizer

    AnalyticsNormalizer = _AnalyticsNormalizer
except Exception:
    AnalyticsNormalizer = None

# Agents: knowledge
KnowledgeRetriever: Any
try:
    from app.agents.knowledge.retriever import KnowledgeRetriever as _KnowledgeRetriever

    KnowledgeRetriever = _KnowledgeRetriever
except Exception:
    KnowledgeRetriever = None

KnowledgeRanker: Any
try:
    from app.agents.knowledge.ranker import KnowledgeRanker as _KnowledgeRanker

    KnowledgeRanker = _KnowledgeRanker
except Exception:
    KnowledgeRanker = None

KnowledgeAnswerer: Any
try:
    from app.agents.knowledge.answerer import KnowledgeAnswerer as _KnowledgeAnswerer

    KnowledgeAnswerer = _KnowledgeAnswerer
except Exception:
    KnowledgeAnswerer = None

# Agents: commerce
CommerceDetector: Any
try:
    from app.agents.commerce.detector import CommerceDetector as _CommerceDetector

    CommerceDetector = _CommerceDetector
except Exception:
    CommerceDetector = None

CommerceExtractor: Any
try:
    from app.agents.commerce.extractor import CommerceExtractor as _CommerceExtractor

    CommerceExtractor = _CommerceExtractor
except Exception:
    CommerceExtractor = None

CommerceSummarizer: Any
try:
    from app.agents.commerce.summarizer import CommerceSummarizer as _CommerceSummarizer

    CommerceSummarizer = _CommerceSummarizer
except Exception:
    CommerceSummarizer = None

# Triage
TriageHandler: Any
try:
    from app.agents.triage.handler import TriageHandler as _TriageHandler

    TriageHandler = _TriageHandler
except Exception:
    TriageHandler = None

# Contracts (optional; used for consistency only)
RouterDecision: Any
try:
    from app.contracts.router_decision import RouterDecision as _RouterDecision

    RouterDecision = _RouterDecision
except Exception:
    RouterDecision = None

Answer: Any
try:
    from app.contracts.answer import Answer as _Answer

    Answer = _Answer
except Exception:
    Answer = None

__all__ = ["build_graph"]

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_graph(*, require_sql_approval: bool = True) -> Any:
    """Build and return a compiled LangGraph (or a descriptive stub).

    Parameters
    ----------
    require_sql_approval: When True, emit a human gate before executing SQL.
    """
    log = get_logger("graph.build")

    # Instantiate components with gentle fallbacks
    classifier = LLMClassifier() if LLMClassifier is not None else _StubClassifier()

    analytics_planner = (
        AnalyticsPlanner() if AnalyticsPlanner is not None else _StubAnalyticsPlanner()
    )
    analytics_executor = (
        AnalyticsExecutor()
        if AnalyticsExecutor is not None
        else _StubAnalyticsExecutor(require_sql_approval)
    )
    analytics_norm = (
        AnalyticsNormalizer() if AnalyticsNormalizer is not None else _StubAnalyticsNormalizer()
    )

    retriever = (
        KnowledgeRetriever() if KnowledgeRetriever is not None else _StubKnowledgeRetriever()
    )
    ranker = KnowledgeRanker() if KnowledgeRanker is not None else _StubKnowledgeRanker()
    answerer = KnowledgeAnswerer() if KnowledgeAnswerer is not None else _StubKnowledgeAnswerer()

    detector = CommerceDetector() if CommerceDetector is not None else _StubCommerceDetector()
    extractor = CommerceExtractor() if CommerceExtractor is not None else _StubCommerceExtractor()
    summarizer = (
        CommerceSummarizer() if CommerceSummarizer is not None else _StubCommerceSummarizer()
    )

    triage = TriageHandler() if TriageHandler is not None else _StubTriageHandler()

    if StateGraph is None:  # Return a descriptive stub for environments without LangGraph
        return {
            "engine": "stub",
            "nodes": [
                "route",
                "supervisor",
                "analytics.plan",
                "analytics.exec",
                "analytics.normalize",
                "knowledge.retrieve",
                "knowledge.rank",
                "knowledge.answer",
                "commerce.detect",
                "commerce.extract",
                "commerce.summarize",
                "triage.handle",
            ],
            "require_sql_approval": bool(require_sql_approval),
        }

    with start_span("graph.build"):
        sg = StateGraph(dict)  # state is a plain mapping

        # -- Node definitions ------------------------------------------------
        def node_route(state: dict[str, Any]) -> dict[str, Any]:
            q = str(state.get("query", "")).strip()
            with start_span("node.route"):
                dec = classifier.classify(q)
                state["router_decision"] = dec
                return state

        def node_supervisor(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.supervisor"):
                dec = state.get("router_decision", {})
                dec2 = apply_routing_rules(dec, allowlist=state.get("allowlist"))
                # Normalize agent name
                agent = (dec2.get("agent") or "triage").strip()
                state["agent"] = agent
                state["router_decision"] = dec2
                return state

        # Analytics pipeline
        def node_an_plan(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.analytics.plan"):
                plan = analytics_planner.plan(
                    query=str(state.get("query", "")),
                    allowlist=state.get("allowlist"),
                )
                state["analytics_plan"] = plan
                return state

        def node_an_exec(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.analytics.exec"):
                plan = state.get("analytics_plan", {})
                sql = plan.get("sql", "")
                params = plan.get("params", {})
                limit = plan.get("limit_applied")

                # Optional human gate
                if require_sql_approval and sql:
                    state.setdefault("interrupts", []).append(
                        make_sql_gate(
                            sql=sql,
                            params=params,
                            limit=limit,
                            tables=plan.get("tables"),
                            reason="Aprovar execução de SQL",
                        )
                    )

                rows = analytics_executor.execute(sql=sql, params=params, limit=limit)
                state["analytics_rows"] = rows
                return state

        def node_an_norm(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.analytics.normalize"):
                rows = state.get("analytics_rows")
                plan = state.get("analytics_plan", {})
                normalized = analytics_norm.normalize(
                    query=str(state.get("query", "")), rows=rows, plan=plan
                )
                state["answer"] = normalized
                return state

        # Knowledge pipeline
        def node_kn_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.knowledge.retrieve"):
                hits = retriever.retrieve(query=str(state.get("query", "")), k=state.get("k", 6))
                state["hits"] = hits
                return state

        def node_kn_rank(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.knowledge.rank"):
                ranked = ranker.rank(query=str(state.get("query", "")), hits=state.get("hits", []))
                state["ranked"] = ranked
                return state

        def node_kn_answer(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.knowledge.answer"):
                ans = answerer.answer(
                    query=str(state.get("query", "")), ranked=state.get("ranked", [])
                )
                state["answer"] = ans
                return state

        # Commerce pipeline
        def node_co_detect(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.commerce.detect"):
                det = detector.detect(
                    source_filename=state.get("source_filename"),
                    source_mime=state.get("source_mime"),
                    text=state.get("text"),
                )
                state["detection"] = det
                return state

        def node_co_extract(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.commerce.extract"):
                det = state.get("detection")
                doc = extractor.extract(
                    text=state.get("text", ""),
                    source_filename=state.get("source_filename"),
                    source_mime=state.get("source_mime"),
                    doc_type_hint=getattr(det, "doc_type", None)
                    or (det.get("doc_type") if isinstance(det, Mapping) else None),
                    currency_hint=getattr(det, "currency", None)
                    or (det.get("currency") if isinstance(det, Mapping) else None),
                )
                state["doc"] = doc
                return state

        def node_co_summarize(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.commerce.summarize"):
                ans = summarizer.summarize(state.get("doc"))
                state["answer"] = ans
                return state

        # Triage
        def node_tr_handle(state: dict[str, Any]) -> dict[str, Any]:
            with start_span("node.triage.handle"):
                ans = triage.handle(query=str(state.get("query", "")), signals=state.get("signals"))
                state["answer"] = ans
                return state

        # -- Graph wiring ----------------------------------------------------
        sg.add_node("route", node_route)
        sg.add_node("supervisor", node_supervisor)

        sg.add_node("analytics.plan", node_an_plan)
        sg.add_node("analytics.exec", node_an_exec)
        sg.add_node("analytics.normalize", node_an_norm)

        sg.add_node("knowledge.retrieve", node_kn_retrieve)
        sg.add_node("knowledge.rank", node_kn_rank)
        sg.add_node("knowledge.answer", node_kn_answer)

        sg.add_node("commerce.detect", node_co_detect)
        sg.add_node("commerce.extract", node_co_extract)
        sg.add_node("commerce.summarize", node_co_summarize)

        sg.add_node("triage.handle", node_tr_handle)

        sg.set_entry_point("route")
        sg.add_edge("route", "supervisor")

        # Conditional fan‑out after supervisor
        sg.add_conditional_edges(
            "supervisor",
            lambda s: (s.get("agent") or "triage").strip(),
            {
                "analytics": "analytics.plan",
                "knowledge": "knowledge.retrieve",
                "commerce": "commerce.detect",
                "triage": "triage.handle",
            },
        )

        # Pipelines
        sg.add_edge("analytics.plan", "analytics.exec")
        sg.add_edge("analytics.exec", "analytics.normalize")
        sg.add_edge("analytics.normalize", END)

        sg.add_edge("knowledge.retrieve", "knowledge.rank")
        sg.add_edge("knowledge.rank", "knowledge.answer")
        sg.add_edge("knowledge.answer", END)

        sg.add_edge("commerce.detect", "commerce.extract")
        sg.add_edge("commerce.extract", "commerce.summarize")
        sg.add_edge("commerce.summarize", END)

        sg.add_edge("triage.handle", END)

        # Compile with optional checkpointer
        compiled = (
            sg.compile(checkpointer=get_checkpointer() if get_checkpointer is not None else None)
            if get_checkpointer is not None
            else sg.compile()
        )

        try:
            log.info(
                "Graph compiled", nodes=list(compiled.nodes) if hasattr(compiled, "nodes") else None
            )
        except Exception:
            pass

        return compiled


# ---------------------------------------------------------------------------
# Local stub implementations (used when agent modules are not available)
# ---------------------------------------------------------------------------
class _StubClassifier:
    def classify(self, query: str) -> dict[str, Any]:
        # Very light heuristic: presence of keywords
        ql = (query or "").lower()
        if any(k in ql for k in ("invoice", "po ", "purchase order", "beo")):
            agent = "commerce"
        elif any(k in ql for k in ("tabela", "coluna", "média", "soma", "por mês", "sql")):
            agent = "analytics"
        elif any(k in ql for k in ("política", "manual", "documento", "pdf", "como ")):
            agent = "knowledge"
        else:
            agent = "triage"
        return {
            "agent": agent,
            "confidence": 0.55,
            "reason": "stub",
            "tables": [],
            "columns": [],
            "signals": [],
        }


class _StubAnalyticsPlanner:
    def plan(self, *, query: str, allowlist: Mapping[str, Any] | None = None) -> dict[str, Any]:
        sql = "SELECT COUNT(*) AS qty FROM orders LIMIT 100"
        return {"sql": sql, "params": {}, "limit_applied": 100, "tables": ["orders"]}


class _StubAnalyticsExecutor:
    def __init__(self, require_sql_approval: bool) -> None:
        self.require_sql_approval = require_sql_approval

    def execute(
        self, *, sql: str, params: Mapping[str, Any] | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        # Return a tiny fake result
        return [{"qty": 123}]


class _StubAnalyticsNormalizer:
    def normalize(self, *, query: str, rows: Any, plan: Mapping[str, Any]) -> Mapping[str, Any]:
        text = "Encontrei 123 registros (amostra limitada para segurança)."
        return {
            "text": text,
            "data": rows,
            "columns": list(rows[0].keys()) if rows else [],
            "meta": {"sql": plan.get("sql")},
        }


class _StubKnowledgeRetriever:
    def retrieve(self, *, query: str, k: int = 6) -> list[dict[str, Any]]:
        return [
            {
                "doc_id": "stub",
                "chunk_id": "0",
                "title": "Guia",
                "text": "Conteúdo relevante.",
                "source": None,
                "score": 0.5,
            }
        ]


class _StubKnowledgeRanker:
    def rank(self, *, query: str, hits: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
        return hits


class _StubKnowledgeAnswerer:
    def answer(self, *, query: str, ranked: list[Mapping[str, Any]]) -> Mapping[str, Any]:
        return {
            "text": "Resumo baseado no documento enviado.",
            "citations": [{"title": "Guia", "doc_id": "stub", "chunk_id": "0", "lines": ""}],
            "meta": {},
        }


class _StubCommerceDetector:
    def detect(
        self, *, source_filename: str | None, source_mime: str | None, text: str | None
    ) -> Mapping[str, Any]:
        return {"doc_type": "invoice", "confidence": 0.6, "currency": "USD"}


class _StubCommerceExtractor:
    def extract(
        self,
        *,
        text: str,
        source_filename: str | None,
        source_mime: str | None,
        doc_type_hint: str | None,
        currency_hint: str | None,
    ) -> Mapping[str, Any]:
        return {
            "doc": {
                "doc_type": doc_type_hint,
                "doc_id": "INV-001",
                "currency": currency_hint or "USD",
            },
            "dates": {"issue_date": "2024-01-01", "due_date": "2024-01-15"},
            "items": [
                {"line_no": 1, "name": "Item A", "qty": 2, "unit_price": 10.0, "line_total": 20.0}
            ],
            "totals": {"grand_total": 20.0},
            "risks": [],
        }


class _StubCommerceSummarizer:
    def summarize(self, doc: Mapping[str, Any]) -> Mapping[str, Any]:
        return {"text": "Fatura INV-001 no valor de US$ 20,00.", "meta": {"doc_id": "INV-001"}}


class _StubTriageHandler:
    def handle(self, query: str, *, signals: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
        return {
            "text": "Preciso de mais contexto. Você pode detalhar?",
            "followups": ["Qual tabela ou documento devo usar?"],
            "meta": {"suggested_agent": "triage"},
        }
