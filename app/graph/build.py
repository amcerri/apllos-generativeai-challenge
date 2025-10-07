"""
Analytics SQL executor (read-only, bounded, timed).

Overview
--------
Executes planner-generated SQL with strict safety guarantees: read-only
transaction, server-side timeout, and client-side row cap. Converts DB rows to
plain dictionaries for downstream normalization.

Design
------
- **Read-only**: `SET LOCAL default_transaction_read_only = on` within a
  transaction. No DDL/DML allowed.
- **Timeout**: `SET LOCAL statement_timeout` (milliseconds).
- **Row cap**: stream rows and stop at `max_rows`, regardless of SQL LIMIT.
- **Explain (optional)**: `EXPLAIN (FORMAT JSON)`; can upgrade to ANALYZE only
  if explicitly enabled via env flag.
- **Zero hard deps**: the module imports `app.infra.db.get_engine()` lazily.
  If infra is absent at import time, it degrades gracefully.

Integration
-----------
- Consumes a plan compatible with `PlannerPlan` (fields: `sql`, `params`,
  `limit_applied`, `reason`).
- Returns an `ExecutorResult` with timing and diagnostics.
- Logging and tracing are optional but supported if infra is available.

Usage
-----
>>> from app.agents.analytics.executor import AnalyticsExecutor
>>> exe = AnalyticsExecutor()
>>> res = exe.execute({"sql": "SELECT 1 AS x", "params": {}}, max_rows=10)
>>> res.row_count, isinstance(res.rows, list)
(1, True)
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

# Initialize logger
log = get_logger(__name__)


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

# Optional metrics (prometheus_client may be absent)
try:
    from app.infra.metrics import inc_counter as _inc_counter, observe_histogram as _observe_hist
except Exception:  # pragma: no cover - optional
    def _inc_counter(_name: str, labels: Mapping[str, str] | None = None, amount: float = 1.0) -> None:
        return
    def _observe_hist(_name: str, value_ms: float, labels: Mapping[str, str] | None = None) -> None:
        return

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
DocumentProcessor: Any
try:
    from app.agents.commerce.processor import DocumentProcessor as _DocumentProcessor

    DocumentProcessor = _DocumentProcessor
except Exception:
    DocumentProcessor = None

LLMCommerceExtractor: Any
try:
    from app.agents.commerce.extractor_llm import LLMCommerceExtractor as _LLMCommerceExtractor

    LLMCommerceExtractor = _LLMCommerceExtractor
except Exception:
    LLMCommerceExtractor = None



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

    # Analytics
    analytics_rows: Annotated[list[Mapping[str, Any]] | None, _pick_last]

    # Knowledge
    hits: Annotated[list[Mapping[str, Any]] | None, _pick_last]
    ranked: Annotated[list[Mapping[str, Any]] | None, _pick_last]
    citations: Annotated[list[Mapping[str, Any]] | None, _pick_last]

    # Commerce
    processed_document: Annotated[Mapping[str, Any] | None, _pick_last]

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
    # Defensive: retry import of KnowledgeAnswerer at build-time to avoid
    # early import ordering/cycles causing stub fallback, without rebinding
    # the module-level symbol (avoid UnboundLocalError).
    _answerer_cls = KnowledgeAnswerer
    if _answerer_cls is None:
        try:
            from app.agents.knowledge.answerer import KnowledgeAnswerer as _RetryKnowledgeAnswerer  # type: ignore
            _answerer_cls = _RetryKnowledgeAnswerer  # type: ignore
            log.info("KnowledgeAnswerer reloaded successfully")
        except Exception as _exc:  # pragma: no cover - optional
            log.warning("Using stub KnowledgeAnswerer", extra={"error": type(_exc).__name__})
            _answerer_cls = None
    if _answerer_cls is None:
        # Fail fast instead of silently returning misleading stub content
        raise RuntimeError("KnowledgeAnswerer unavailable; cannot build knowledge pipeline")
    answerer = _answerer_cls()

    document_processor = DocumentProcessor() if DocumentProcessor is not None else _StubDocumentProcessor()
    llm_extractor = LLMCommerceExtractor() if LLMCommerceExtractor is not None else _StubLLMCommerceExtractor()
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
            "commerce.process_doc",
            "commerce.extract_llm",
            "commerce.summarize",
                "triage.handle",
            ],
            "require_sql_approval": bool(require_sql_approval),
        }

    with start_span("graph.build"):
        sg = StateGraph(GraphState)  # typed state with channels

        # -- Node definitions (return deltas only) ---------------------------
        def node_route(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
            q = str(state.get("query", "")).strip()
            attachment = state.get("attachment")
            
            # If there's an attachment, modify the query to include attachment context
            if attachment:
                filename = attachment.get("filename", "arquivo")
                content_preview = attachment.get("content", "")[:200] + "..." if len(attachment.get("content", "")) > 200 else attachment.get("content", "")
                q = f"{q} (Anexo: {filename} - {content_preview})"
            
            log.info("Route node debug", 
                    original_query=q,
                    has_attachment=bool(attachment))
            
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
                
                out = {
                    "allowlist": allowlist or {},  # Include allowlist in state
                    "router_decision": dec_dict,
                    "tables": list(dec_dict.get("tables", [])),
                    "columns": list(dec_dict.get("columns", [])),
                    "signals": list(dec_dict.get("signals", [])),
                }
            _inc_counter("requests_total", {"agent": "router", "node": "route"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "route"})
            return out

        def node_supervisor(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.supervisor"):
                log.info("Supervisor node called", 
                        router_decision=state.get("router_decision"),
                        state_keys=list(state.keys()))
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
                out = {"agent": agent, "router_decision": dec2_dict}
            _inc_counter("requests_total", {"agent": "routing", "node": "supervisor"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "supervisor"})
            return out

        # Analytics pipeline
        def node_an_plan(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
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
                out = {"analytics_plan": plan}
            _inc_counter("requests_total", {"agent": "analytics", "node": "plan"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "analytics.plan"})
            return out

        def node_an_exec(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
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

                # If there was an approval interrupt and it was rejected upstream,
                # execute in dry-run mode (EXPLAIN-only) to surface diagnostics.
                dry_run = False
                try:
                    interrupts = state.get("interrupts") or []
                    for intr in interrupts:
                        if intr.get("type") == "human_interrupt" and intr.get("name") == "sql_execution":
                            human = state.get("human_response")  # type: ignore[assignment]
                            if isinstance(human, dict) and human.get("approved") is False:
                                dry_run = True
                                break
                except Exception:
                    dry_run = False

                rows = analytics_executor.execute(plan_dict, dry_run=dry_run, include_explain=True)
                out["analytics_rows"] = rows
                _inc_counter("requests_total", {"agent": "analytics", "node": "exec"})
                _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "analytics.exec"})
                return out

        def node_an_norm(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
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
                out = {"answer": normalized}
            _inc_counter("requests_total", {"agent": "analytics", "node": "normalize"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "analytics.normalize"})
            return out

        # Knowledge pipeline
        def node_kn_retrieve(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.knowledge.retrieve"):
                result = retriever.retrieve(query=str(state.get("query", "")), top_k=state.get("k", 6), min_score=0.01)
                out = {"hits": result.hits}
            _inc_counter("requests_total", {"agent": "knowledge", "node": "retrieve"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "knowledge.retrieve"})
            return out

        def node_kn_rank(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.knowledge.rank"):
                result = ranker.rank(query=str(state.get("query", "")), hits=state.get("hits") or [])
                out = {"ranked": result.hits}
            _inc_counter("requests_total", {"agent": "knowledge", "node": "rank"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "knowledge.rank"})
            return out

        def node_kn_answer(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.knowledge.answer"):
                ans = answerer.answer(
                    query=str(state.get("query", "")), ranked=state.get("ranked") or []
                )
                cites = ans.get("citations") if isinstance(ans, dict) else None
                out: dict[str, Any] = {"answer": ans}
                if cites:
                    out["citations"] = cites
                _inc_counter("requests_total", {"agent": "knowledge", "node": "answer"})
                _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "knowledge.answer"})
                return out

        # Commerce pipeline
        def node_co_process_doc(state: GraphState) -> dict[str, Any]:
            """Process attachment and extract text."""
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.commerce.process_doc"):
                attachment = state.get("attachment")
                
                # Check if attachment is valid (has both filename and content)
                has_valid_attachment = attachment and attachment.get("filename") and attachment.get("content")
                
                # Debug logging
                log.info("Commerce process_doc debug", 
                        has_attachment=bool(attachment),
                        has_valid_attachment=has_valid_attachment)
                
                # If no valid attachment, return error
                if not has_valid_attachment:
                    log.info("No valid attachment, returning error")
                    return {"processed_document": {"text": "", "success": False, "warnings": ["no_attachment"]}}
                
                # Process attachment
                # Enforce simple attachment guardrails (size/mime) before processing
                try:
                    max_size_mb = 50
                    size = int((attachment.get("metadata", {}) or {}).get("size", 0))
                    if size and size > max_size_mb * 1024 * 1024:
                        return {"processed_document": {"text": "", "success": False, "warnings": ["attachment_too_large"]}}
                    # MIME/type constraints when provided
                    allowed_mimes = {
                        "application/pdf",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "application/msword",
                        "text/plain",
                        "image/png",
                        "image/jpeg",
                        "image/tiff",
                        "image/bmp",
                    }
                    mt = str(attachment.get("mime_type") or "").strip()
                    if mt and mt not in allowed_mimes:
                        return {"processed_document": {"text": "", "success": False, "warnings": ["unsupported_mime"]}}
                except Exception:
                    pass
                result = document_processor.process_attachment(attachment)
                out = {"processed_document": result}
            _inc_counter("requests_total", {"agent": "commerce", "node": "process_doc"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "commerce.process_doc"})
            return out

        def node_co_extract_llm(state: GraphState) -> dict[str, Any]:
            """Extract structured data using LLM."""
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.commerce.extract_llm"):
                processed = state.get("processed_document", {})
                text = processed.get("text", "")
                metadata = processed.get("metadata", {})
                
                if not text or not processed.get("success", False):
                    return {"processed_document": processed}
                
                # Extract using LLM
                document = llm_extractor.extract(text=text, metadata=metadata)
                
                # Update processed document with extraction result
                processed["document"] = document
                out = {"processed_document": processed}
            _inc_counter("requests_total", {"agent": "commerce", "node": "extract_llm"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "commerce.extract_llm"})
            return out



        def node_co_summarize(state: GraphState) -> dict[str, Any]:
            """Summarize processed document."""
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.commerce.summarize"):
                processed = state.get("processed_document", {})
                document = processed.get("document")
                
                if not document:
                    return {"answer": {"text": "❌ Erro ao processar documento.", "meta": {"error": "no_document"}}}
                
                # Generate summary
                ans = summarizer.summarize(document)
                
                # Add processing info to metadata
                if isinstance(ans, dict) and "meta" in ans:
                    ans["meta"]["processing_method"] = processed.get("method", "unknown")
                    ans["meta"]["processing_warnings"] = processed.get("warnings", [])

                out = {"answer": ans}
            _inc_counter("requests_total", {"agent": "commerce", "node": "summarize"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "commerce.summarize"})
            return out

        # Triage
        def node_tr_handle(state: GraphState) -> dict[str, Any]:
            import time as _t
            _t0 = _t.perf_counter()
            with start_span("node.triage.handle"):
                ans = triage.handle(query=str(state.get("query", "")), signals=state.get("signals"))
                out = {"answer": ans}
            _inc_counter("requests_total", {"agent": "triage", "node": "handle"})
            _observe_hist("node_latency_ms", (_t.perf_counter() - _t0) * 1000.0, {"node": "triage.handle"})
            return out

        # -- Graph wiring ----------------------------------------------------
        sg.add_node("route", node_route)
        sg.add_node("supervisor", node_supervisor)

        sg.add_node("analytics.plan", node_an_plan)
        sg.add_node("analytics.exec", node_an_exec)
        sg.add_node("analytics.normalize", node_an_norm)

        sg.add_node("knowledge.retrieve", node_kn_retrieve)
        sg.add_node("knowledge.rank", node_kn_rank)
        sg.add_node("knowledge.answer", node_kn_answer)

        sg.add_node("commerce.process_doc", node_co_process_doc)
        sg.add_node("commerce.extract_llm", node_co_extract_llm)
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
                "commerce": "commerce.process_doc",
                "triage": "triage.handle",
            },
        )
        
        # Commerce routing: always go to extract_llm after processing
        sg.add_edge("commerce.process_doc", "commerce.extract_llm")

        # Pipelines
        sg.add_edge("analytics.plan", "analytics.exec")
        sg.add_edge("analytics.exec", "analytics.normalize")
        sg.add_edge("analytics.normalize", END)

        sg.add_edge("knowledge.retrieve", "knowledge.rank")
        sg.add_edge("knowledge.rank", "knowledge.answer")
        sg.add_edge("knowledge.answer", END)

        sg.add_edge("commerce.extract_llm", "commerce.summarize")
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


class _StubDocumentProcessor:
    def process_attachment(self, attachment: dict[str, Any]) -> dict[str, Any]:
        return {
            "text": "Invoice #INV-001\nItem A: 1x $20.00 = $20.00\nTotal: $20.00",
            "metadata": {"filename": "stub.pdf", "method": "stub"},
            "method": "stub",
            "warnings": [],
            "success": True
        }


class _StubLLMCommerceExtractor:
    def extract(self, *, text: str, metadata: dict[str, Any] | None = None, **kwargs) -> dict[str, Any]:
        return {
            "doc": {
                "doc_type": "invoice",
                "doc_id": "INV-001",
                "currency": "USD",
            },
            "dates": {"issue_date": "2024-01-01", "due_date": "2024-01-15"},
            "items": [{"name": "Item A", "qty": 1, "unit_price": 20.0, "line_total": 20.0}],
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