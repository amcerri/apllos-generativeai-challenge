"""
Graph builder (LangGraph wiring for multi-agent assistant).

Overview
--------
Assemble a LangGraph graph that routes user requests across four specialized
agents (analytics, knowledge, commerce, triage) using a context-first
supervisor. The build is dependency-light and degrades gracefully if LangGraph
is not available, returning a descriptive stub for tests.

Design
------
- Optional imports for LangGraph; provide safe fallbacks.
- Nodes wrap our agent components with minimal, business-centric I/O.
- Routing: LLM classifier → deterministic supervisor with single-pass fallbacks.
- Human-in-the-loop: optional SQL approval gate emitted before execution.
- Checkpointing: integrated when available via the infra helper.
- Typed state with per-key channels (Annotated reducers) to support concurrent
  updates during Studio graph rendering.

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
from typing import Any, Annotated, TypedDict

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

# Optional messages reducer (Studio draws may fan-out and merge)
try:
    from langgraph.graph.message import add_messages as _add_messages

    add_messages = _add_messages  # type: ignore[assignment]
except Exception:  # pragma: no cover - optional

    def add_messages(left: list[dict] | None, right: list[dict] | None) -> list[dict]:
        # Fallback concatenation used only when LangGraph is absent at import time.
        return (left or []) + (right or [])


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
        reason: str = "Approve SQL execution",
    ) -> dict[str, Any]:
        return {
            "type": "human_interrupt",
            "name": "sql_execution",
            "details": {
                "sql": sql,
                "params": dict(params or {}),
                "limit": limit,
                "tables": list(tables or []),
                "reason": reason,
            },
        }


# Router & Supervisor
LLMClassifier: Any
try:
    from app.routing.llm_classifier import LLMClassifier as _LLMClassifier

    LLMClassifier = _LLMClassifier
except Exception:  # pragma: no cover - optional
    LLMClassifier = None

supervise: Any
try:
    from app.routing.supervisor import supervise as _supervise

    supervise = _supervise
except Exception:  # pragma: no cover - optional

    def supervise(
        decision: Mapping[str, Any], *, allowlist: Mapping[str, list[str]] | None = None
    ) -> Mapping[str, Any]:
        return decision


# Agents: analytics - use full LLM-powered planner
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


# ---------------------------------------------------------------------------
# Reducers (channels) to tolerate fan-out during Studio graph drawing
# ---------------------------------------------------------------------------
def _pick_last(_left: Any | None, right: Any | None) -> Any | None:
    """Reducer: keep the last writer's value."""
    return right


# Reducer: concatenates lists, tolerating None on either side.
def _concat_list(left: list[Any] | None, right: list[Any] | None) -> list[Any]:
    """Reducer: concatenates lists, tolerating None on either side."""
    return (left or []) + (right or [])


# ---------------------------------------------------------------------------
# Graph state definition (typed) with per-key channels
# ---------------------------------------------------------------------------
class GraphState(TypedDict, total=False):
    # Input / routing
    query: Annotated[str, _pick_last]
    attachment: Annotated[Mapping[str, Any] | None, _pick_last]
    allowlist: Annotated[Mapping[str, Sequence[str]] | None, _pick_last]
    router_decision: Annotated[Mapping[str, Any] | None, _pick_last]
    agent: Annotated[str | None, _pick_last]
    tables: Annotated[list[str], _pick_last]
    columns: Annotated[list[str], _pick_last]
    k: Annotated[int | None, _pick_last]

    # Observability / multi-writers
    signals: Annotated[list[str], _concat_list]
    interrupts: Annotated[list[dict[str, Any]], _concat_list]
    messages: Annotated[list[dict[str, Any]], add_messages]

    # Analytics
    analytics_plan: Annotated[Mapping[str, Any] | None, _pick_last]
    sql: Annotated[str | None, _pick_last]
    params: Annotated[Mapping[str, Any] | None, _pick_last]
    limit: Annotated[int | None, _pick_last]
    analytics_rows: Annotated[list[Mapping[str, Any]] | None, _pick_last]

    # Knowledge
    hits: Annotated[list[Mapping[str, Any]] | None, _pick_last]
    ranked: Annotated[list[Mapping[str, Any]] | None, _pick_last]
    citations: Annotated[list[Mapping[str, Any]] | None, _pick_last]

    # Commerce
    detection: Annotated[Mapping[str, Any] | None, _pick_last]
    doc: Annotated[Mapping[str, Any] | None, _pick_last]

    # Final answer
    answer: Annotated[Mapping[str, Any] | None, _pick_last]


__all__ = ["build_graph"]

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_graph(*, require_sql_approval: bool = True, allowlist: dict[str, Any] | None = None) -> Any:
    """Build and return a compiled LangGraph (or a descriptive stub).

    Parameters
    ----------
    require_sql_approval: When True, emit a human gate before executing SQL.
    """
    log = get_logger("graph.build")

    # Database configuration is handled globally in assistant.py

    # Allowlist will be loaded in assistant.py and passed via state

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
        sg = StateGraph(GraphState)  # typed state with channels

        # -- Node definitions (return deltas only) ---------------------------
        def node_route(state: GraphState) -> dict[str, Any]:
            q = str(state.get("query", "")).strip()
            attachment = state.get("attachment")
            
            # If there's an attachment, modify the query to include attachment context
            if attachment:
                filename = attachment.get("filename", "arquivo")
                content_preview = attachment.get("content", "")[:200] + "..." if len(attachment.get("content", "")) > 200 else attachment.get("content", "")
                q = f"{q} (Anexo: {filename} - {content_preview})"
            
            with start_span("node.route"):
                dec = classifier.classify(q)
                # Convert RouterDecision to dict if it's a dataclass
                if hasattr(dec, '__dict__'):
                    dec_dict = dec.__dict__
                else:
                    dec_dict = dec
                
                # Ensure we can access attributes as dict keys
                if not isinstance(dec_dict, dict):
                    dec_dict = {
                        "agent": getattr(dec, "agent", "triage"),
                        "confidence": getattr(dec, "confidence", 0.0),
                        "reason": getattr(dec, "reason", ""),
                        "tables": getattr(dec, "tables", []),
                        "columns": getattr(dec, "columns", []),
                        "signals": getattr(dec, "signals", []),
                        "thread_id": getattr(dec, "thread_id", ""),
                    }
                
                return {
                    "allowlist": allowlist or {},  # Include allowlist in state
                    "router_decision": dec_dict,
                    "tables": list(dec_dict.get("tables", [])),
                    "columns": list(dec_dict.get("columns", [])),
                    "signals": list(dec_dict.get("signals", [])),
                }

        def node_supervisor(state: GraphState) -> dict[str, Any]:
            with start_span("node.supervisor"):
                dec = state.get("router_decision") or {}
                # Don't pass context to avoid incorrect fallbacks
                dec2 = supervise(dec)
                # Convert RouterDecision to dict if it's a dataclass
                if hasattr(dec2, '__dict__'):
                    dec2_dict = dec2.__dict__
                else:
                    dec2_dict = dec2
                
                # Ensure we can access attributes as dict keys
                if not isinstance(dec2_dict, dict):
                    dec2_dict = {
                        "agent": getattr(dec2, "agent", "triage"),
                        "confidence": getattr(dec2, "confidence", 0.0),
                        "reason": getattr(dec2, "reason", ""),
                        "tables": getattr(dec2, "tables", []),
                        "columns": getattr(dec2, "columns", []),
                        "signals": getattr(dec2, "signals", []),
                        "thread_id": getattr(dec2, "thread_id", ""),
                    }
                
                # Ensure dec2_dict is not None
                if dec2_dict is None:
                    dec2_dict = {"agent": "triage", "confidence": 0.0, "reason": "", "tables": [], "columns": [], "signals": []}
                
                agent = (dec2_dict.get("agent") or "triage").strip()
                return {"agent": agent, "router_decision": dec2_dict}

        # Analytics pipeline
        def node_an_plan(state: GraphState) -> dict[str, Any]:
            with start_span("node.analytics.plan"):
                allowlist = state.get("allowlist") or {}
                # Fallback to hardcoded allowlist if empty
                if not allowlist:
                    allowlist = {
                        "orders": ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"],
                        "order_items": ["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"],
                        "customers": ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"],
                        "products": ["product_id", "product_category_name", "product_name_lenght", "product_description_lenght", "product_photos_qty", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"],
                        "sellers": ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"],
                        "order_payments": ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"],
                        "order_reviews": ["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message", "review_creation_date", "review_answer_timestamp"],
                        "geolocation": ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng", "geolocation_city", "geolocation_state"],
                        "product_category_translation": ["product_category_name", "product_category_name_english"]
                    }
                plan = analytics_planner.plan(
                    query=str(state.get("query", "")),
                    allowlist=allowlist,
                )
                return {"analytics_plan": plan}

        def node_an_exec(state: GraphState) -> dict[str, Any]:
            with start_span("node.analytics.exec"):
                plan = state.get("analytics_plan")
                if plan is None:
                    return {"rows": [], "sql": "", "error": "No analytics plan available"}
                
                # Convert PlannerPlan to dict if needed
                if hasattr(plan, 'to_dict'):
                    plan_dict = plan.to_dict()
                elif hasattr(plan, '__dict__'):
                    plan_dict = plan.__dict__
                else:
                    plan_dict = plan
                
                sql = plan_dict.get("sql", "")
                params = plan_dict.get("params", {})
                limit = plan_dict.get("limit_applied")
                out: dict[str, Any] = {}

                if require_sql_approval and sql:
                    out["interrupts"] = [
                        make_sql_gate(
                            sql=sql,
                            params=params,
                            limit=limit,
                            tables=plan_dict.get("tables"),
                            reason="Approve SQL execution",
                        )
                    ]

                rows = analytics_executor.execute(plan_dict)
                out["analytics_rows"] = rows
                return out

        def node_an_norm(state: GraphState) -> dict[str, Any]:
            with start_span("node.analytics.normalize"):
                result = state.get("analytics_rows")
                plan = state.get("analytics_plan") or {}
                
                # Convert plan to dict if needed
                if hasattr(plan, 'to_dict'):
                    plan_dict = plan.to_dict()
                elif hasattr(plan, '__dict__'):
                    plan_dict = plan.__dict__
                else:
                    plan_dict = plan
                
                # Convert ExecutorResult to dict if needed
                if hasattr(result, 'to_dict'):
                    result_dict = result.to_dict()
                elif hasattr(result, '__dict__'):
                    result_dict = result.__dict__
                else:
                    result_dict = result or {}
                
                normalized = analytics_norm.normalize(
                    plan=plan_dict,
                    result=result_dict,
                    question=str(state.get("query", ""))
                )
                return {"answer": normalized}

        # Knowledge pipeline
        def node_kn_retrieve(state: GraphState) -> dict[str, Any]:
            with start_span("node.knowledge.retrieve"):
                result = retriever.retrieve(query=str(state.get("query", "")), top_k=state.get("k", 6), min_score=0.01)
                return {"hits": result.hits}

        def node_kn_rank(state: GraphState) -> dict[str, Any]:
            with start_span("node.knowledge.rank"):
                result = ranker.rank(query=str(state.get("query", "")), hits=state.get("hits") or [])
                return {"ranked": result.hits}

        def node_kn_answer(state: GraphState) -> dict[str, Any]:
            with start_span("node.knowledge.answer"):
                ans = answerer.answer(
                    query=str(state.get("query", "")), ranked=state.get("ranked") or []
                )
                cites = ans.get("citations") if isinstance(ans, dict) else None
                out: dict[str, Any] = {"answer": ans}
                if cites:
                    out["citations"] = cites
                return out

        # Commerce pipeline
        def node_co_detect(state: GraphState) -> dict[str, Any]:
            with start_span("node.commerce.detect"):
                det = detector.detect(
                    source_filename=state.get("source_filename"),
                    source_mime=state.get("source_mime"),
                    text=state.get("text"),
                )
                return {"detection": det}

        def node_co_extract(state: GraphState) -> dict[str, Any]:
            with start_span("node.commerce.extract"):
                det = state.get("detection") or {}
                doc = extractor.extract(
                    text=str(state.get("text", "")),
                    source_filename=state.get("source_filename"),
                    source_mime=state.get("source_mime"),
                    doc_type_hint=getattr(det, "doc_type", None)
                    or (det.get("doc_type") if isinstance(det, Mapping) else None),
                    currency_hint=getattr(det, "currency", None)
                    or (det.get("currency") if isinstance(det, Mapping) else None),
                )
                return {"doc": doc}

        def node_co_summarize(state: GraphState) -> dict[str, Any]:
            with start_span("node.commerce.summarize"):
                ans = summarizer.summarize(state.get("doc") or {})
                return {"answer": ans}

        # Triage
        def node_tr_handle(state: GraphState) -> dict[str, Any]:
            with start_span("node.triage.handle"):
                ans = triage.handle(query=str(state.get("query", "")), signals=state.get("signals"))
                return {"answer": ans}

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

        # Conditional fan-out after supervisor
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
        elif any(k in ql for k in ("tabela", "coluna", "média", "soma", "por mês", "sql", "pedido")):
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

    def execute(self, plan: Mapping[str, Any]) -> list[dict[str, Any]]:
        # Return a tiny fake result
        return [{"qty": 123}]


class _StubAnalyticsNormalizer:
    def normalize(self, plan: Mapping[str, Any], result: Mapping[str, Any], question: str) -> Mapping[str, Any]:
        text = "Encontrei 123 registros (amostra limitada para segurança)."
        rows = result.get("rows", [])
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