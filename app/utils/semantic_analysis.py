"""
Semantic query analysis for intelligent data display decisions.

Overview
  Provides semantic analysis of user queries to determine optimal data display
  strategy. Analyzes query intent, type, and context to decide whether to show
  complete data or intelligent summaries.

Design
  - LLM-first approach for semantic analysis (language-agnostic)
  - Pattern-based fallback when LLM unavailable
  - Query type detection (distribution, top-N, temporal, aggregation)
  - Intent analysis (explicit vs implicit data requests)

Integration
  - Used by Analytics normalizer for intelligent data display decisions
  - Integrates with LLM client for semantic analysis
  - Works with conversation context when available

Usage
  >>> from app.utils.semantic_analysis import SemanticQueryAnalyzer
  >>> analyzer = SemanticQueryAnalyzer()
  >>> analysis = analyzer.analyze_query("Quantos pedidos temos por estado?")
  >>> analysis["query_type"]
  'distribution'
"""

from __future__ import annotations

import re
from typing import Any

try:
    from app.infra.logging import get_logger
except Exception:
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:
    from app.infra.llm_client import get_llm_client
except Exception:
    get_llm_client = None

__all__ = ["SemanticQueryAnalyzer"]


class SemanticQueryAnalyzer:
    """Semantic analysis of queries for intelligent data display decisions."""

    def __init__(self) -> None:
        """Initialize semantic query analyzer."""
        self.log = get_logger(__name__)
        self._llm_client = None

        try:
            if get_llm_client:
                self._llm_client = get_llm_client()
        except Exception:
            pass

    def analyze_query(
        self,
        query: str,
        row_count: int = 0,
        conversation_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Analyze query semantics to determine optimal data display strategy.

        Parameters
        ----------
        query
            User query text.
        row_count
            Number of rows in the result set.
        conversation_context
            Optional conversation context for follow-up queries.

        Returns
        -------
        dict[str, Any]
            Analysis result with query_type, intent, and display_strategy.
        """
        if not query or not query.strip():
            return {
                "query_type": "unknown",
                "intent": "unknown",
                "display_strategy": "summary",
                "should_show_complete": False,
            }

        # Try LLM-first approach for semantic analysis
        if self._llm_client and self._llm_client.is_available():
            try:
                llm_analysis = self._analyze_with_llm(query, row_count, conversation_context)
                if llm_analysis:
                    return llm_analysis
            except Exception as exc:
                self.log.debug("LLM semantic analysis failed, using fallback", extra={"error": str(exc)})

        # Fallback to pattern-based analysis
        return self._analyze_with_patterns(query, row_count)

    def _analyze_with_llm(
        self,
        query: str,
        row_count: int,
        conversation_context: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Analyze query semantics using LLM."""
        try:
            context_info = ""
            if conversation_context:
                last_answer = conversation_context.get("last_answer")
                if last_answer:
                    context_info = f"\nCONTEXTO: Última resposta foi sobre {last_answer.get('text', '')[:100]}"

            analysis_prompt = f"""Analyze the user query to determine:
1. Query type (distribution, top_n, temporal, aggregation, count, correlation)
2. Intent (explicit_all, implicit_all, analysis, summary)
3. Display strategy (complete_data, intelligent_summary, analysis_only)

QUERY: "{query}"
ROW COUNT: {row_count}
{context_info}

QUERY TYPES:
- "distribution": Queries asking for data grouped by categories (states, categories, etc.)
- "top_n": Queries asking for top N items
- "temporal": Queries asking for time series or trends over time
- "aggregation": Queries asking for aggregated metrics (averages, totals, etc.)
- "count": Simple count queries
- "correlation": Queries asking for relationships between metrics

INTENT:
- "explicit_all": User explicitly asks for "all", "each", "every", "complete list"
- "implicit_all": User asks for distribution/grouping but doesn't explicitly say "all"
- "analysis": User asks for analysis, insights, patterns, trends
- "summary": User asks for summary or overview

DISPLAY STRATEGY:
- "complete_data": Show all data points (for distributions with <= 100 items, or when explicitly requested)
- "intelligent_summary": Show summary with key insights and sample data
- "analysis_only": Focus on analysis and insights, minimal raw data

EXAMPLES:
- "Quantos pedidos temos por estado?" → type: distribution, intent: implicit_all, strategy: complete_data (if <= 100 states)
- "Mostre todos os estados" → type: distribution, intent: explicit_all, strategy: complete_data
- "Identifique padrões nos dados" → type: correlation, intent: analysis, strategy: analysis_only
- "Top 10 produtos" → type: top_n, intent: implicit_all, strategy: complete_data

Return JSON: {{"query_type": "string", "intent": "string", "display_strategy": "string", "should_show_complete": bool, "reason": "string"}}
"""

            response = self._llm_client.chat_completion(
                messages=[{"role": "user", "content": analysis_prompt}],
                model="gpt-4o-mini",
                temperature=0.0,
                max_tokens=200,
                response_format={"type": "json_object"},
            )

            if response and response.text:
                result = self._llm_client.extract_json(response.text)
                if result:
                    return {
                        "query_type": result.get("query_type", "unknown"),
                        "intent": result.get("intent", "unknown"),
                        "display_strategy": result.get("display_strategy", "intelligent_summary"),
                        "should_show_complete": result.get("should_show_complete", False),
                        "reason": result.get("reason", ""),
                    }
        except Exception as exc:
            self.log.debug("LLM analysis failed", extra={"error": str(exc)})

        return None

    def _analyze_with_patterns(self, query: str, row_count: int) -> dict[str, Any]:
        """Fallback pattern-based analysis."""
        q = query.lower().strip()

        # Detect query type
        query_type = "unknown"
        if any(p in q for p in ["por estado", "por categoria", "por região", "por vendedor", "por transportadora"]):
            query_type = "distribution"
        elif any(p in q for p in ["top", "maiores", "menores", "melhores", "piores"]):
            query_type = "top_n"
        elif any(p in q for p in ["por mês", "por dia", "por ano", "temporal", "tendência", "evolução"]):
            query_type = "temporal"
        elif any(p in q for p in ["correlação", "relação", "impacto", "influência"]):
            query_type = "correlation"
        elif any(p in q for p in ["quantos", "quantidade", "total", "soma", "média"]):
            query_type = "aggregation"

        # Detect intent
        intent = "unknown"
        explicit_all_patterns = [
            "todos os",
            "cada",
            "todos",
            "completo",
            "toda a lista",
            "todos os estados",
            "cada estado",
        ]
        if any(p in q for p in explicit_all_patterns):
            intent = "explicit_all"
        elif any(p in q for p in ["análise", "analise", "insights", "padrões", "tendências"]):
            intent = "analysis"
        elif query_type == "distribution":
            intent = "implicit_all"

        # Determine display strategy
        should_show_complete = False
        display_strategy = "intelligent_summary"

        if intent == "explicit_all" and row_count <= 100:
            should_show_complete = True
            display_strategy = "complete_data"
        elif query_type == "top_n":
            should_show_complete = True
            display_strategy = "complete_data"
        elif query_type == "distribution" and row_count <= 50:
            should_show_complete = True
            display_strategy = "complete_data"
        elif intent == "analysis":
            display_strategy = "analysis_only"
            should_show_complete = False

        return {
            "query_type": query_type,
            "intent": intent,
            "display_strategy": display_strategy,
            "should_show_complete": should_show_complete,
            "reason": "pattern_based_analysis",
        }

