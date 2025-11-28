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
        """
        Return an Answer-like object with guidance and follow-ups.

        Args:
            query: The raw user query.
            signals: Optional router/supervisor signals to refine hints.

        Returns:
            Answer-like object with text, meta, and followups.

        Raises:
            ValueError: If query is empty or invalid.
        """
        with start_span("agent.triage.handle"):
            agent, reasons = triage_suggested_agent(query, signals)
            sig_list = _signals_to_list(signals)
            text = _compose_text_ptbr(query, agent, signals=sig_list)
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


def _compose_text_ptbr(query: str, agent: str, *, signals: list[str] | None = None) -> str:
    q = (query or "").strip()

    # --- Detect meta questions FIRST -----------------------------------------
    meta_type = _detect_meta_question(q)
    if meta_type:
        return _compose_detailed_capabilities_response(q, meta_type)

    # --- Detect greeting -----------------------------------------------------
    if _looks_like_greeting(q):
        return _greeting_with_capabilities()

    # --- Detect out-of-scope topics -----------------------------------------
    # Check signals first (from router), then fall back to local detection
    sigs = set(signals or [])
    oos_topic = None
    if "out_of_scope" in sigs:
        # Router already detected out-of-scope; try to read the topic label
        for sig in sigs:
            if sig != "out_of_scope":
                oos_topic = sig
                break
    if not oos_topic:
        # No explicit topic from router, detect from query as a best-effort fallback.
        oos_topic = _detect_out_of_scope(q)
    
    if oos_topic:
        # Map signal names to human-readable topic names when using standard labels.
        topic_map = {
            "weather": "previsão do tempo/meteorologia",
            "news": "notícias em tempo real",
            "financial_markets": "cotações/mercado financeiro em tempo real",
            "code_generation": "geração de código fora do contexto do projeto",
            "sports_entertainment": "assuntos esportivos/entretenimento",
        }
        topic_display = topic_map.get(oos_topic, oos_topic)
        
        # Prefer a humanized LLM message; fallback to a concise fixed text
        human = _human_oos_message(q, topic_display)
        fallback = f"No momento não ofereço {topic_display}. Sugiro consultar um serviço especializado."
        msg = human or fallback
        return msg + "\n\n" + _capabilities_block() + "\n\nComo posso ajudar?"

    # --- Default contextual nudge based on suggested agent -------------------
    base = (
        "Ainda não tenho contexto suficiente para responder com precisão. "
        "Vou te direcionar para o melhor caminho."
    )
    # Be explicit when router marked ambiguity/low confidence
    sigs = set(signals or [])
    if ("low_confidence" in sigs) or ("ambiguous_intent" in sigs):
        base = (
            "Fiquei em dúvida sobre a intenção (dados x documentos). "
            "Com um detalhe rápido, eu acerto o melhor caminho."
        )
    if agent == "analytics":
        hint = (
            "Parece uma análise sobre dados tabulares. Se puder, informe a tabela/colunas, "
            "a métrica e o período que deseja."
        )
    elif agent == "knowledge":
        hint = (
            "Parece uma pergunta respondível por conteúdo já documentado. "
            "Se puder, informe o tema ou termos‑chave para eu buscar nas fontes disponíveis."
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
    lead = f'Pedido: "{q}"\n' if q else ""
    return lead + base + " " + hint + "\n\n" + _capabilities_block() + "\n\nComo posso ajudar?"


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
# Local intent helpers for triage rendering
# ---------------------------------------------------------------------------


def _looks_like_greeting(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return False
    greetings = (
        "oi",
        "olá",
        "ola",
        "bom dia",
        "boa tarde",
        "boa noite",
        "tudo bem",
        "e aí",
        "eaí",
        "hello",
        "hi",
    )
    return any(g in t for g in greetings)


def _greeting_with_capabilities() -> str:
    import datetime as _dt
    hour = _dt.datetime.now().hour
    if 5 <= hour < 12:
        sal = "Bom dia"
    elif 12 <= hour < 18:
        sal = "Boa tarde"
    else:
        sal = "Boa noite"
    return f"{sal}! Em que posso ajudar?\n\n" + _capabilities_block()


def _detect_out_of_scope(text: str) -> str | None:
    t = (text or "").lower().strip()
    if not t:
        return None

    ecommerce_terms = (
        "e-commerce",
        "ecommerce",
        "loja virtual",
        "loja online",
        "marketplace",
        "pedido",
        "pedidos",
        "carrinho",
        "checkout",
        "cliente",
        "clientes",
        "entrega",
        "frete",
        "venda",
        "vendas",
        "faturamento",
    )

    def _has_ecommerce_signals() -> bool:
        return any(term in t for term in ecommerce_terms)

    weather = ("previsão do tempo", "previsao do tempo", "meteorologia", "clima", "tempo em ")
    news = ("notícias", "noticias", "news")
    markets = ("bolsa de valores", "ações", "dólar", "euro", "stock", "forex")
    code = ("programar em", "escreva um código", "write code")
    sports = ("futebol", "jogo", "basquete", "vôlei", "volei", "nba", "fifa", "champions", "copa do mundo")

    if any(k in t for k in weather) and not _has_ecommerce_signals():
        return "previsão do tempo/meteorologia"
    if any(k in t for k in news) and not _has_ecommerce_signals():
        return "notícias em tempo real"
    if any(k in t for k in markets) and not _has_ecommerce_signals():
        return "cotações/mercado financeiro em tempo real"
    if any(k in t for k in code):
        return "geração de código fora do contexto do projeto"
    if any(k in t for k in sports):
        return "assuntos esportivos/entretenimento"
    return None


def _capabilities_block() -> str:
    return (
        "Minhas funcionalidades incluem:\n"
        "- Consultar informações em **bancos de dados**\n"
        "- Buscar respostas em **bases de conhecimento**\n"
        "- Extrair e analisar dados de arquivos PDF, DOCX, ou TXT\n\n"
    )


def _detect_meta_question(query: str) -> str | None:
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

    import re

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


def _compose_detailed_capabilities_response(query: str, meta_type: str) -> str:
    """Generate detailed response about system capabilities or usage guidance.

    This function is only called when a meta question is explicitly detected.
    It provides detailed information about system capabilities or usage guidance
    based on the type of meta question asked.

    Parameters
    ----------
    query:
        User query text.
    meta_type:
        Type of meta question ("capabilities" or "usage").

    Returns
    -------
    str
        Detailed response text in Portuguese.
    """
    if meta_type == "capabilities":
        return _detailed_capabilities_text()
    elif meta_type == "usage":
        return _detailed_usage_guidance(query)
    else:
        # Fallback to capabilities if meta type is unknown
        return _detailed_capabilities_text()


def _detailed_capabilities_text() -> str:
    """Generate detailed text about system capabilities.

    This detailed description is only shown when explicitly requested
    by the user (meta questions about system capabilities).
    """
    return """Sou um assistente multi-agente especializado em e-commerce. Minhas funcionalidades incluem:

**Analytics Agent** - Análise de Dados
- Consultar dados do banco de dados usando linguagem natural
- Gerar consultas SQL seguras e otimizadas
- Calcular métricas, agregações e análises estatísticas
- Análises temporais (por mês, dia, trimestre)
- Correlações e análises de tendências
- Exemplos: "Quantos pedidos temos este mês?", "Qual a média de tempo de entrega por estado?"

**Knowledge Agent** - Base de Conhecimento (RAG)
- Buscar informações em documentos e guias
- Responder perguntas conceituais sobre e-commerce
- Explicar políticas, procedimentos e melhores práticas
- Fornecer respostas baseadas em documentação disponível
- Exemplos: "O que é taxa de recompra?", "Como funciona o processo de embalagem?"

**Commerce Agent** - Processamento de Documentos
- Extrair dados estruturados de documentos comerciais
- Processar invoices, notas fiscais, purchase orders, BEOs
- Analisar documentos PDF, DOCX, TXT e imagens (com OCR)
- Identificar totais, itens, datas e informações relevantes
- Exemplos: Envie um PDF de invoice e eu extraio os dados estruturados

**Como usar:**
- Para dados: Pergunte diretamente (ex: "Quantos pedidos temos?")
- Para conhecimento: Faça perguntas conceituais (ex: "O que é taxa de conversão?")
- Para documentos: Anexe o arquivo e descreva o que precisa

Como posso ajudar você hoje?"""


def _detailed_usage_guidance(query: str) -> str:
    """Generate usage guidance based on query content.

    Parameters
    ----------
    query:
        User query text.

    Returns
    -------
    str
        Detailed usage guidance text in Portuguese.
    """
    q = (query or "").lower()

    if any(term in q for term in ["pedido", "order", "dados", "data", "banco", "database", "sql"]):
        return """**Como consultar pedidos e dados no banco:**

1. **Faça perguntas em linguagem natural** sobre os dados que deseja:
   - "Quantos pedidos temos este mês?"
   - "Qual a média de tempo de entrega por estado?"
   - "Mostre as vendas por categoria nos últimos 3 meses"

2. **Seja específico sobre:**
   - **Tabela/Coluna**: Se souber, mencione (ex: "na tabela orders")
   - **Período**: Especifique o período (ex: "este mês", "último trimestre")
   - **Agrupamento**: Se quiser agrupar (ex: "por estado", "por categoria")
   - **Métricas**: O que quer calcular (ex: "média", "soma", "contagem")

3. **O sistema irá:**
   - Gerar SQL seguro automaticamente
   - Executar a consulta no banco de dados
   - Retornar os dados formatados e com análise interpretativa

**Exemplos práticos:**
- "Quantos pedidos temos?" → Contagem total de pedidos
- "Tempo médio de entrega por transportadora" → Análise agrupada
- "Vendas por estado nos últimos 6 meses" → Análise temporal e geográfica

Precisa de ajuda com alguma consulta específica?"""

    elif any(term in q for term in ["documento", "document", "pdf", "invoice", "nota", "fatura"]):
        return """**Como processar documentos comerciais:**

1. **Anexe o arquivo** (PDF, DOCX, TXT ou imagem)
2. **Descreva o tipo de documento** (opcional, mas ajuda):
   - Invoice/Nota Fiscal
   - Purchase Order (PO)
   - Banquet Event Order (BEO)
   - Recibo ou Cotação

3. **O sistema irá:**
   - Extrair texto do documento (com OCR se necessário)
   - Identificar campos estruturados (totais, itens, datas)
   - Fornecer resumo estruturado dos dados
   - Oferecer opção de integrar no sistema (futuro)

**Exemplos:**
- Anexe um PDF de invoice → Extração automática de dados
- Anexe uma nota fiscal → Identificação de itens e totais

Tem algum documento para processar?"""

    elif any(term in q for term in ["conhecimento", "knowledge", "documentação", "documentation", "guia", "manual"]):
        return """**Como buscar informações na base de conhecimento:**

1. **Faça perguntas conceituais** sobre e-commerce:
   - "O que é taxa de recompra?"
   - "Como funciona o processo de embalagem?"
   - "Qual a melhor estratégia para frete?"

2. **O sistema irá:**
   - Buscar documentos relevantes na base de conhecimento
   - Sintetizar resposta baseada na documentação
   - Fornecer citações das fontes

**Exemplos:**
- "O que é taxa de conversão?" → Explicação conceitual
- "Como melhorar o tempo de entrega?" → Guia baseado em documentação

Tem alguma pergunta conceitual sobre e-commerce?"""

    else:
        return _detailed_capabilities_text()


# ---------------------------------------------------------------------------
# LLM helpers for humanized out-of-scope messages
# ---------------------------------------------------------------------------


def _human_oos_message(query: str, topic: str) -> str | None:
    """Return a brief, empathetic PT-BR message for out-of-scope requests using LLM.

    Falls back to None if LLM is unavailable or errors, so callers can use a fixed string.
    """
    try:
        from app.infra.llm_client import get_llm_client  # local import; optional
        client = get_llm_client()
        if not client.is_available():
            return None

        system = (
            "Você é um assistente educado em pt-BR. Dê uma única resposta curta e humana, "
            "reconhecendo gentilmente que o pedido está fora do escopo do sistema atual e sugerindo "
            "consultar um site/app/serviço especializado. A resposta deve levar em conta o pedido "
            "real do usuário e o tópico de fora de escopo identificado.\n\n"
            "Regras de estilo:\n"
            "- Responder em pt-BR.\n"
            "- Sem listas, sem markdown, 1–2 frases no máximo.\n"
            "- Tom profissional, empático e direto.\n"
            "- Não prometa funcionalidades que o sistema não possui.\n"
        )
        user = (
            "Pedido original do usuário (fora de escopo):\n"
            f"{(query or '').strip()}\n\n"
            f"Tópico de fora de escopo identificado: {topic or 'genérico'}.\n\n"
            "Responda de forma breve, clara e empática, explicando por que não pode atender "
            "esse tipo de pedido e sugerindo que o usuário consulte um serviço especializado "
            "(por exemplo, site de meteorologia, portal de notícias, corretora, etc.)."
        )
        resp = client.chat_completion(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            model=getattr(client, "model", "gpt-4o-mini"),
            temperature=0.2,
            max_tokens=120,
            max_retries=0,
        )
        text = (resp.text if resp else "").strip()
        # Guard: trim overly long output
        if len(text) > 320:
            text = text[:319].rstrip() + "…"
        return text or None
    except Exception:
        return None


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
