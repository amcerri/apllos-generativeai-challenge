"""
Triage handler (business guidance and redirection).

Overview
--------
Provide a short, business-friendly PT‑BR response when a user request lacks
context or does not clearly map to analytics/knowledge/commerce. The handler
suggests the most likely agent based on lightweight heuristics and offers
2–3 objective follow-ups to unlock routing.

Design
------
- Pure, dependency-light module using the shared logging/tracing infrastructure
  if available.
- Heuristics consider the user query (keywords) and optional router signals
  (e.g., allowlist/table/column hints, rag_hits, doc signals).
- Output conforms to the `Answer` contract when available; otherwise a dict with equivalent fields is returned (keys: text, meta, followups).

Integration
-----------
- Used by the `triage` agent when the classifier confidence is low or the
  context-first guardrails cannot pick a definitive path.

Usage
-----
>>> from app.agents.triage.handler import TriageHandler
>>> h = TriageHandler()
>>> out = h.handle("me mostre vendas por mês")
>>> isinstance(out, dict) or hasattr(out, "text")
True
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final

try:  # Optional logger
    from app.infra.logging import get_logger as _get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def _get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


# Tracing (optional; single alias to avoid mypy signature clashes)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# Optional Answer dataclass
ANSWER_CLS: Any
try:
    from app.contracts.answer import Answer as _Answer

    ANSWER_CLS = _Answer
except Exception:  # pragma: no cover - optional
    ANSWER_CLS = None

__all__ = ["TriageHandler", "triage_suggested_agent"]


# ---------------------------------------------------------------------------
# Signal normalization helpers
# ---------------------------------------------------------------------------

def _signals_to_mapping(signals: object) -> dict[str, Any]:
    """Normalize arbitrary `signals` into a dict[str, Any].

    Accepts Mapping, Sequence (of primitives), or scalars. This guards
    against `dict(list[str])` ValueErrors when callers pass a list.
    """
    if signals is None:
        return {}
    if isinstance(signals, Mapping):
        # Ensure plain dict[str, Any]
        return {str(k): signals[k] for k in signals.keys()}
    if isinstance(signals, Sequence) and not isinstance(signals, str | bytes | bytearray):
        return {"signals": [str(x) for x in signals]}
    return {"signals": [str(signals)]}


def _signals_to_list(signals: object) -> list[str]:
    """Coerce arbitrary `signals` input to a list[str] for Answer.meta."""
    if signals is None:
        return []
    if isinstance(signals, Mapping):
        return [str(k) for k in signals.keys()]
    if isinstance(signals, Sequence) and not isinstance(signals, str | bytes | bytearray):
        return [str(x) for x in signals]
    return [str(signals)]


# ---------------------------------------------------------------------------
# Lightweight heuristics
# ---------------------------------------------------------------------------
_ANALYTICS_TERMS: Final[tuple[str, ...]] = (
    "tabela",
    "coluna",
    "colunas",
    "agrupar",
    "agrupamento",
    "por mês",
    "por dia",
    "média",
    "soma",
    "top",
    "sql",
    "query",
    "taxa de conversão",
    "coorte",
)

_KNOWLEDGE_TERMS: Final[tuple[str, ...]] = (
    "política",
    "manual",
    "documento",
    "pdf",
    "guia",
    "procedimento",
    "como",
    "o que",
)

_COMMERCE_TERMS: Final[tuple[str, ...]] = (
    "invoice",
    "nota fiscal",
    "fatura",
    "purchase order",
    "po ",
    "po#",
    "beo",
    "banquet event order",
    "order form",
    "cotação",
    "proposta",
    "recibo",
)


def triage_suggested_agent(
    query: str, signals: Mapping[str, Any] | Sequence[Any] | None = None
) -> tuple[str, list[str]]:
    """Suggest an agent (analytics|knowledge|commerce|triage) and reasons.

    Heuristic order respects the project's context-first rules: if textual/doc‑
    like → knowledge; if tabular/metrics → analytics; if commercial-doc hints →
    commerce; otherwise triage.
    """

    ql = (query or "").lower().strip()
    reasons: list[str] = []

    # Signals from router can short-circuit
    s = _signals_to_mapping(signals)
    if s.get("rag_hits"):
        reasons.append("router_signal:rag_hits")
        return "knowledge", reasons
    if s.get("allowlist_tables") or s.get("allowlist_columns"):
        reasons.append("router_signal:analytics_allowlist_overlap")
        return "analytics", reasons
    if s.get("doc_signals"):
        reasons.append("router_signal:commerce_doc_signals")
        return "commerce", reasons

    def _has_any(terms: tuple[str, ...]) -> bool:
        return any(t in ql for t in terms)

    if _has_any(_KNOWLEDGE_TERMS):
        reasons.append("keyword:knowledge")
        return "knowledge", reasons
    if _has_any(_ANALYTICS_TERMS):
        reasons.append("keyword:analytics")
        return "analytics", reasons
    if _has_any(_COMMERCE_TERMS):
        reasons.append("keyword:commerce")
        return "commerce", reasons

    return "triage", reasons


# ---------------------------------------------------------------------------
# Handler
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class TriageHandler:
    """Produce a PT‑BR guidance answer with suggested next steps."""

    def handle(self, query: str, *, signals: Mapping[str, Any] | Sequence[Any] | None = None) -> Any:
        """Return an Answer-like object with guidance and follow-ups.

        Parameters
        ----------
        query: The raw user query.
        signals: Optional router/supervisor signals to refine hints.
        """
        with start_span("agent.triage.handle"):
            agent, reasons = triage_suggested_agent(query, signals)
            sig_list = _signals_to_list(signals)
            text = _compose_text_ptbr(query, agent)
            payload = {
                "text": text,
                "meta": {
                    "suggested_agent": agent,
                    "reasons": reasons,
                    "signals": sig_list,
                },
                "followups": _followups_for(agent),
            }
            return _coerce_answer(payload)


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def _compose_text_ptbr(query: str, agent: str) -> str:
    base = (
        "Ainda não tenho contexto suficiente para responder com precisão. "
        "Vou te direcionar para o melhor caminho."
    )
    if agent == "analytics":
        hint = (
            "Parece uma análise sobre dados tabulares. Se puder, informe a tabela/colunas, "
            "a métrica e o período que deseja."
        )
    elif agent == "knowledge":
        hint = (
            "Parece uma pergunta respondível por documentos. Se tiver, anexe o PDF/TXT "
            "ou indique o título do material."
        )
    elif agent == "commerce":
        hint = (
            "Parece um documento comercial (invoice/PO/BEO/etc.). Se puder, envie o arquivo "
            "ou detalhe o tipo e o total esperado."
        )
    else:
        hint = (
            "Me diga se busca dados (tabelas/colunas), uma informação de documento (PDF/guia) "
            "ou análise de um arquivo comercial (invoice/PO)."
        )
    q = (query or "").strip()
    lead = f'Pedido: "{q}"\n' if q else ""
    return lead + base + " " + hint


def _followups_for(agent: str) -> list[str]:
    if agent == "analytics":
        return [
            "Qual tabela e colunas devo usar?",
            "Qual métrica/agrupamento (ex.: pedidos por mês)?",
            "Qual período e filtros deseja aplicar?",
        ]
    if agent == "knowledge":
        return [
            "Pode anexar o PDF/TXT ou indicar o título do documento?",
            "Qual seção ou tópico devo priorizar?",
            "Precisa de um resumo ou de passos práticos?",
        ]
    if agent == "commerce":
        return [
            "Qual o tipo do documento (invoice, PO, BEO, recibo)?",
            "Pode compartilhar o arquivo para extração estruturada?",
            "Qual o total esperado para validarmos?",
        ]
    return [
        "É sobre dados (tabelas/colunas), documentos (PDF/guia) ou um arquivo comercial?",
        "Há algum período, número de pedido ou produto específico?",
        "Deseja que eu dê exemplos do que posso fazer?",
    ]


# ---------------------------------------------------------------------------
# Answer coercion
# ---------------------------------------------------------------------------


def _coerce_answer(dec: Mapping[str, Any]) -> Any:
    if ANSWER_CLS is None:
        return dict(dec)
    try:
        if hasattr(ANSWER_CLS, "from_dict"):
            return ANSWER_CLS.from_dict(dec)
        if hasattr(ANSWER_CLS, "from_mapping"):
            return ANSWER_CLS.from_mapping(dec)
        return ANSWER_CLS(**dec)
    except Exception:
        return dict(dec)
