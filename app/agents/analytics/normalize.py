"""
Analytics normalizer (business-friendly Portuguese narration).

Overview
--------
Convert the raw rows produced by the analytics executor into a user-facing
`Answer` object (or plain mapping) with:
- Natural PT‑BR narrative (`text`) tailored to the query shape (count,
  time series, preview/top‑N).
- Optional tabular payload (`data`, `columns`).
- Diagnostics in `meta` (SQL, row_count, limit flags, timings).

Design
------
- Pure Python (no third‑party deps), type‑annotated and lint‑friendly.
- Shape inference by inspecting output columns (e.g., `period`, `qty`).
- Conservative formatting: locale‑like number formatting for PT‑BR and
  ISO‑like dates for data payload stability.

Integration
-----------
- Called by the analytics agent after executing the planner SQL.
- Accepts a `plan` (dict‑like with `sql`, `limit_applied`) and a `result`
  (dict‑like with `rows`, `row_count`, `exec_ms`, `limit_applied`).
- Returns a dataclass `Answer` if available; else a plain `dict` with the
  same fields.

Usage
-----
>>> from app.agents.analytics.normalize import AnalyticsNormalizer
>>> norm = AnalyticsNormalizer()
>>> ans = norm.normalize(
...     plan={"sql": "SELECT COUNT(1) AS qty FROM orders", "limit_applied": False},
...     result={"rows": [{"qty": 42}], "row_count": 1, "exec_ms": 3.2, "limit_applied": False},
...     question="Quantos pedidos existem?",
... )
>>> isinstance(ans, dict) or hasattr(ans, "text")
True
"""

from __future__ import annotations

import re
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Final, cast
from pathlib import Path

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:  # Optional config
    from app.config.settings import get_settings
except Exception:  # pragma: no cover - optional
    def get_settings():
        return None


# Tracing (optional; keep a single alias)
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

__all__ = ["AnalyticsNormalizer"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class _PlanView:
    sql: str
    limit_applied: bool


@dataclass(slots=True)
class _ResultView:
    rows: list[Mapping[str, Any]]
    row_count: int
    exec_ms: float
    limit_applied: bool


class AnalyticsNormalizer:
    """LLM-powered analytics normalizer using structured prompts."""

    def __init__(self) -> None:
        self.log = get_logger("agent.analytics.normalize")
        self._system_prompt = self._load_system_prompt()
        self._examples = self._load_examples()
    

    def _load_system_prompt(self) -> str:
        """Load system prompt from prompts folder; fallback to embedded.

        Returns
        -------
        str
            System prompt content for the LLM normalizer.
        """
        try:
            base = Path(__file__).parent.parent.parent / "prompts" / "analytics" / "normalizer_system.txt"
            content = base.read_text(encoding="utf-8")
            return content
        except Exception:
            return self._fallback_system_prompt()
    
    def _load_examples(self) -> list[dict[str, Any]]:
        """Load few-shot examples from prompts if available; otherwise empty.

        Returns
        -------
        list[dict[str, Any]]
            Example pairs with keys {"input", "output"}.
        """
        try:
            examples_path = Path(__file__).parent.parent.parent / "prompts" / "analytics" / "normalizer_examples.jsonl"
            out: list[dict[str, Any]] = []
            with examples_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        out.append(json.loads(line))
            return out
        except Exception:
            return []


    def normalize(
        self,
        *,
        plan: Mapping[str, Any] | _PlanView,
        result: Mapping[str, Any] | _ResultView,
        question: str | None = None,
    ) -> Any:
        """
        Normalize using LLM-powered approach with fallback.

        Args:
            plan: Plan view containing SQL and limit information.
            result: Result view containing rows, count, and execution metadata.
            question: Original user question for context.

        Returns:
            Answer-like object with formatted text and metadata.

        Raises:
            ValueError: If plan or result data is invalid.
            RuntimeError: If normalization fails completely.
        """
        
        # Convert inputs to standard format
        plan_view = _as_plan(plan)
        result_view = _as_result(result)
        user_query = question or "Consulta de dados"
        
        # Always try LLM first for human-like responses
        try:
            llm_result = self._normalize_with_llm(user_query, plan_view, result_view)
            if llm_result:
                return _coerce_answer(llm_result)
            else:
                self.log.warning("LLM normalization returned None, using fallback")
                return self._fallback_normalize(user_query, plan_view, result_view)
        except Exception as e:
            # Log the error and use fallback
            self.log.warning(f"LLM normalization failed: {e}, using fallback")
            return self._fallback_normalize(user_query, plan_view, result_view)
    
    
    def _fallback_system_prompt(self) -> str:
        """Fallback system prompt if file loading fails."""
        return """You are an Analytics Result Normalizer. Format SQL results into business-friendly Portuguese responses.
        
        Rules:
        1. Format currency as R$ X,XX
        2. Use thousands separators for large numbers
        3. Provide complete, contextual responses
        4. Return JSON with 'text' field containing the formatted response
        5. Include 'meta' field with query information
        """
    
    def _normalize_with_llm(
        self, 
        user_query: str, 
        plan: _PlanView, 
        result: _ResultView
    ) -> dict[str, Any] | None:
        """Use LLM to normalize the results with response caching."""
        
        # Check response cache first
        try:
            from app.infra.cache import ResponseCache
            
            # Use singleton response cache instance
            if not hasattr(self, "_response_cache"):
                self._response_cache = ResponseCache(ttl_seconds=3600, max_size=1000)
            
            cache = self._response_cache
            cache_key_context = {
                "sql": plan.sql,
                "row_count": result.row_count,
                "limit_applied": result.limit_applied,
            }
            cached = cache.get(user_query, "analytics", context=cache_key_context)
            if cached is not None:
                self.log.debug("Using cached analytics response")
                return cached
        except Exception:
            pass
        
        # Use centralized LLM client (with retries/timeouts handled there)
        try:
            from app.infra.llm_client import get_llm_client
            client = get_llm_client()
            if not client.is_available():
                self.log.warning("LLM client not available")
                return None
        except Exception as exc:
            self.log.warning(f"LLM client init failed: {exc}")
            return None
        
        # Get configuration
        config = get_settings()
        if config is None:
            # Fallback to hardcoded values if config not available
            model = "gpt-4o-mini"
            max_tokens = 800
            temperature = 0.1
            max_examples = 1
        else:
            # Honor model tier switches
            model = config.models.analytics_normalizer.name
            max_tokens = config.models.analytics_normalizer.max_tokens
            temperature = config.models.analytics_normalizer.temperature
            max_examples = config.analytics.normalizer.max_examples_in_prompt
            if getattr(config.models, "enable_normalizer_llm", True) is False:
                return None
        
        # Prepare compact input for LLM (convert non-serializable types)
        def convert_for_json(obj):
            from decimal import Decimal
            from datetime import datetime, date, timedelta
            if isinstance(obj, dict):
                return {k: convert_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_for_json(item) for item in obj]
            elif isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, timedelta):
                return str(obj)  # Convert to string representation
            else:
                return obj
        
        # For large datasets, use a sample for LLM processing but show all data in response
        sample_size = min(50, len(result.rows)) if result.rows else 0
        sample_rows = result.rows[:sample_size] if result.rows else []
        
        input_data = {
            "user_query": user_query,
            "sql": plan.sql,
            "rows": convert_for_json(sample_rows),  # Convert non-serializable types - use sample for LLM
            "row_count": result.row_count,
            "limit_applied": result.limit_applied,
            "has_more_data": len(result.rows) > sample_size
        }
        
        # Build compact messages
        messages = [
            {"role": "system", "content": self._system_prompt}
        ]
        
        
        # Add examples based on configuration
        if self._examples and max_examples > 0:
            for example in self._examples[:max_examples]:
                messages.append({
                    "role": "user", 
                    "content": json.dumps(example["input"], ensure_ascii=False)
                })
                messages.append({
                    "role": "assistant", 
                    "content": json.dumps(example["output"], ensure_ascii=False)
                })
        
        # Add current query
        messages.append({
            "role": "user",
            "content": json.dumps(input_data, ensure_ascii=False)
        })
        
        # Call LLM with configured parameters
        try:
            resp = client.chat_completion(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                # Ask for plain JSON object to simplify parsing
                response_format={"type": "json_object"},
                max_retries=0,
            )
            response_text = (resp.text if resp else "").strip()
        except Exception as e:
            self.log.warning(f"LLM API call failed: {e}")
            return None
        
        # Parse response
        # Prefer centralized JSON extraction helper
        response_data = None
        try:
            response_data = client.extract_json(response_text)
        except Exception:
            response_data = None
        if response_data is None:
            # Try to extract JSON from fenced blocks as a last resort
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    response_data = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    response_data = None
        if response_data is None:
            self.log.warning("LLM response could not be parsed as JSON")
            return None
        
        # Cache the response
        try:
            if hasattr(self, "_response_cache"):
                cache = self._response_cache
                cache_key_context = {
                    "sql": plan.sql,
                    "row_count": result.row_count,
                    "limit_applied": result.limit_applied,
                }
                cache.set(user_query, "analytics", response_data, context=cache_key_context)
        except Exception:
            pass
        
        # For large datasets, let the LLM handle the formatting completely
        # Don't append additional data as the LLM should handle everything
        
        return response_data
    
    def _format_all_data(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Format all data for large datasets with intelligent summarization."""
        if not rows:
            return ""
        
        # For very large datasets (>100 rows), provide intelligent analysis instead of raw data
        if len(rows) > 100:
            return self._format_large_dataset_analysis(rows, user_query)
        
        # For medium datasets (50-100 rows), show key insights + sample data
        if len(rows) > 50:
            return self._format_medium_dataset_analysis(rows, user_query)
        
        # For small datasets, show all data with proper formatting
        return self._format_small_dataset_data(rows)
    
    def _format_large_dataset_analysis(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Provide intelligent analysis for large datasets instead of raw data listing."""
        if not rows:
            return ""
        
        # Analyze the data structure to determine the best summarization approach
        first_row = rows[0]
        
        # Check for temporal/seasonal patterns
        if 'period' in first_row or 'month' in first_row or 'year' in first_row:
            return self._analyze_temporal_patterns(rows, user_query)
        
        # Check for state/category distributions
        if 'state' in first_row and 'category' in first_row:
            return self._analyze_penetration_patterns(rows, user_query)
        elif 'state' in first_row:
            return self._analyze_state_distribution(rows, user_query)
        elif 'category' in first_row:
            return self._analyze_category_distribution(rows, user_query)
        
        # Generic large dataset analysis
        return self._analyze_generic_patterns(rows, user_query)
    
    def _format_medium_dataset_analysis(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Show key insights + sample data for medium datasets."""
        if not rows:
            return ""
        
        # Get top performers and key insights
        insights = self._get_key_insights(rows)
        
        # Detect patterns and add intelligent insights
        pattern_insights = self._detect_patterns_and_insights(rows, user_query)
        
        # Show sample of data (top 25 items for better coverage)
        sample_size = min(25, len(rows))
        sample_data = self._format_small_dataset_data(rows[:sample_size], user_query)
        
        if len(rows) > sample_size:
            sample_data += f"\n\n(Exibindo {sample_size} de {len(rows)} registros - análise completa acima)"
        
        return insights + pattern_insights + "\n\n" + sample_data
    
    def _format_small_dataset_data(self, rows: list[Mapping[str, Any]], user_query: str = "") -> str:
        """Format small datasets with all data shown."""
        if not rows:
            return ""
        
        # Detect patterns and add intelligent insights for small datasets too
        pattern_insights = self._detect_patterns_and_insights(rows, user_query)
        
        text_parts = ["\n\nDados completos:"]
        for i, row in enumerate(rows, 1):
            values = []
            for k, v in row.items():
                if v is not None:
                    if isinstance(v, (int, float)) and v > 1000:
                        values.append(f"{k}: {v:,.0f}")
                    else:
                        values.append(f"{k}: {v}")
            if values:
                text_parts.append(f"{i}. {', '.join(values)}")
        
        return pattern_insights + "\n".join(text_parts)
    
    def _format_complete_data(self, rows: list[Mapping[str, Any]], user_query: str = "") -> str:
        """Format complete data for queries that need all results."""
        if not rows:
            return ""
        
        # Detect patterns and add intelligent insights
        pattern_insights = self._detect_patterns_and_insights(rows, user_query)
        
        text_parts = ["\n\nDados completos:"]
        for i, row in enumerate(rows, 1):
            values = []
            for k, v in row.items():
                if v is not None:
                    if isinstance(v, (int, float)) and v > 1000:
                        values.append(f"{k}: {v:,.0f}")
                    else:
                        values.append(f"{k}: {v}")
            if values:
                text_parts.append(f"{i}. {', '.join(values)}")
        
        return pattern_insights + "\n".join(text_parts)
    
    def _should_show_complete_data(self, user_query: str, result_view: _ResultView) -> bool:
        """Use heuristics and LLM to decide if complete data should be shown or intelligent analysis."""
        try:
            # Quick heuristics for obvious cases
            # Get threshold from config or use default
            try:
                from app.config.settings import get_settings
                config = get_settings()
                if config and hasattr(config, 'analytics') and hasattr(config.analytics, 'complete_data_threshold'):
                    threshold = config.analytics.complete_data_threshold
                else:
                    threshold = 100  # Default threshold
            except:
                threshold = 100  # Fallback threshold
            
            if result_view.row_count <= threshold:
                return True  # Small datasets always show complete
            
            if result_view.row_count > 5000:
                return False  # Very large datasets always use analysis
            
            # Minimal heuristics for obvious cases only (20% keyword assistance)
            query_lower = user_query.lower()
            
            # Only the most obvious cases - very few keywords
            # BUT: Only for small datasets (<= 200 records)
            obvious_complete_patterns = [
                'todos os estados', 'cada estado', 'cada categoria', 'todos os vendedores'
            ]
            
            obvious_analysis_patterns = [
                'identifique padrões', 'identificar padrões', 'padrões sazonais',
                'tendências de crescimento', 'análise de tendências'
            ]
            
            # Check only the most obvious cases
            for pattern in obvious_analysis_patterns:
                if pattern in query_lower:
                    self.log.info(f"Found obvious analysis pattern '{pattern}' in query")
                    return False
            
            # Only apply complete data patterns for small datasets (<= threshold records)
            for pattern in obvious_complete_patterns:
                if pattern in query_lower and result_view.row_count <= threshold:
                    self.log.info(f"Found obvious complete data pattern '{pattern}' in query (small dataset: {result_view.row_count} records)")
                    return True
            
            # Use LLM for most cases (80% LLM decision)
            decision_prompt = f"""
Analise a consulta do usuário e determine se deve mostrar TODOS os dados ou usar análise inteligente.

CONSULTA: "{user_query}"
NÚMERO DE REGISTROS: {result_view.row_count}

REGRAS CLARAS:
- MOSTRAR TODOS: Quando o usuário pede métricas específicas por grupo (ex: "tempo médio por transportadora", "vendas por categoria")
- ANÁLISE INTELIGENTE: Quando o usuário pede insights, padrões, tendências (ex: "identifique padrões", "tendências de crescimento")

DECISÃO:
- Se a consulta pede "tempo médio por X", "vendas por X", "penetração por X" → MOSTRAR TODOS
- Se a consulta pede "identifique padrões", "tendências", "insights" → ANÁLISE INTELIGENTE
- Se a consulta pede métricas específicas por grupo → MOSTRAR TODOS
- Se a consulta pede análise de padrões/tendências → ANÁLISE INTELIGENTE

EXEMPLOS ESPECÍFICOS:
- "tempo médio por transportadora" → MOSTRAR TODOS (métricas específicas)
- "identifique padrões sazonais" → ANÁLISE INTELIGENTE (insights)
- "penetração por estado" → MOSTRAR TODOS (métricas específicas)
- "crescimento trimestre a trimestre" → ANÁLISE INTELIGENTE (tendências)

Responda APENAS com uma das opções: MOSTRAR_TODOS ou ANALISE_INTELIGENTE
"""
            
            from app.infra.llm_client import get_llm_client
            llm = get_llm_client()
            
            response = llm.extract_json(
                prompt=decision_prompt,
                response_format={"type": "json_object", "schema": {
                    "type": "object",
                    "properties": {
                        "decision": {"type": "string", "enum": ["MOSTRAR_TODOS", "ANALISE_INTELIGENTE"]}
                    },
                    "required": ["decision"]
                }}
            )
            
            decision = response.get("decision", "ANALISE_INTELIGENTE")
            self.log.info(f"LLM decision for query '{user_query}': {decision}")
            self.log.info(f"LLM response: {response}")
            return decision == "MOSTRAR_TODOS"
            
        except Exception as e:
            self.log.warning(f"Decision logic failed: {e}, using intelligent analysis")
            return False
    
    def _analyze_temporal_patterns(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Analyze temporal/seasonal patterns for large datasets."""
        if not rows:
            return ""
        
        # Group by time periods and analyze patterns
        from collections import defaultdict
        period_data = defaultdict(list)
        
        for row in rows:
            period = row.get('period', row.get('month', row.get('year', 'Unknown')))
            # Extract numeric values for analysis
            numeric_values = []
            for k, v in row.items():
                if k not in ['period', 'month', 'year'] and isinstance(v, (int, float)):
                    numeric_values.append((k, v))
            
            if numeric_values:
                period_data[period] = numeric_values
        
        # Find top periods and trends
        total_periods = len(period_data)
        top_periods = sorted(period_data.items(), key=lambda x: sum(v[1] for v in x[1]), reverse=True)[:5]
        
        text_parts = [f"\n\nAnálise de padrões temporais ({total_periods} períodos analisados):"]
        
        # Show top performing periods
        text_parts.append("\nPeríodos com maior atividade:")
        for period, values in top_periods:
            total_value = sum(v[1] for v in values)
            text_parts.append(f"  {period}: {total_value:,.0f}")
        
        # Identify trends
        if len(period_data) > 1:
            periods = list(period_data.keys())
            if len(periods) >= 2:
                first_period = periods[0]
                last_period = periods[-1]
                text_parts.append(f"\nPeríodo analisado: {first_period} a {last_period}")
        
        return "\n".join(text_parts)
    
    def _analyze_penetration_patterns(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Analyze penetration patterns for large datasets."""
        if not rows:
            return ""
        
        from collections import defaultdict
        state_data = defaultdict(dict)
        category_totals = defaultdict(float)
        
        for row in rows:
            state = row.get('state', 'Unknown')
            category = row.get('category', 'Unknown')
            penetration = row.get('penetration', 0)
            
            if state is None or category is None:
                continue
                
            state_data[state][category] = penetration
            category_totals[category] += penetration
        
        # Find top states and categories
        top_states = sorted(state_data.items(), key=lambda x: sum(x[1].values()), reverse=True)[:5]
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        text_parts = [f"\n\nAnálise de penetração ({len(state_data)} estados, {len(category_totals)} categorias):"]
        
        # Top performing states
        text_parts.append("\nEstados com maior penetração:")
        for state, categories in top_states:
            total_penetration = sum(categories.values())
            text_parts.append(f"  {state}: {total_penetration:,.0f}")
        
        # Top categories
        text_parts.append("\nCategorias com maior penetração:")
        for category, total in top_categories:
            text_parts.append(f"  {category}: {total:,.0f}")
        
        return "\n".join(text_parts)
    
    def _analyze_state_distribution(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Analyze state distribution for large datasets."""
        if not rows:
            return ""
        
        from collections import defaultdict
        state_totals = defaultdict(float)
        
        for row in rows:
            state = row.get('state', 'Unknown')
            if state is None:
                continue
            
            # Sum all numeric values for this state
            for k, v in row.items():
                if k != 'state' and isinstance(v, (int, float)):
                    state_totals[state] += v
        
        # Top states
        top_states = sorted(state_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        
        text_parts = [f"\n\nAnálise por estado ({len(state_totals)} estados):"]
        text_parts.append("\nTop 10 estados:")
        for state, total in top_states:
            text_parts.append(f"  {state}: {total:,.0f}")
        
        return "\n".join(text_parts)
    
    def _analyze_category_distribution(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Analyze category distribution for large datasets."""
        if not rows:
            return ""
        
        from collections import defaultdict
        category_totals = defaultdict(float)
        
        for row in rows:
            category = row.get('category', 'Unknown')
            if category is None:
                continue
            
            # Sum all numeric values for this category
            for k, v in row.items():
                if k != 'category' and isinstance(v, (int, float)):
                    category_totals[category] += v
        
        # Top categories
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        
        text_parts = [f"\n\nAnálise por categoria ({len(category_totals)} categorias):"]
        text_parts.append("\nTop 10 categorias:")
        for category, total in top_categories:
            text_parts.append(f"  {category}: {total:,.0f}")
        
        return "\n".join(text_parts)
    
    def _analyze_generic_patterns(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Generic analysis for large datasets."""
        if not rows:
            return ""
        
        # Find numeric columns and analyze patterns
        numeric_columns = []
        if rows:
            first_row = rows[0]
            for k, v in first_row.items():
                if isinstance(v, (int, float)):
                    numeric_columns.append(k)
        
        if not numeric_columns:
            return f"\n\nAnálise de {len(rows)} registros (dados não numéricos)"
        
        # Calculate totals and averages for each numeric column
        totals = {col: 0 for col in numeric_columns}
        for row in rows:
            for col in numeric_columns:
                if isinstance(row.get(col), (int, float)):
                    totals[col] += row[col]
        
        text_parts = [f"\n\nAnálise de {len(rows)} registros:"]
        text_parts.append("\nTotais por métrica:")
        for col, total in totals.items():
            if total > 1000:
                text_parts.append(f"  {col}: {total:,.0f}")
            else:
                text_parts.append(f"  {col}: {total:,.2f}")
        
        return "\n".join(text_parts)
    
    def _get_key_insights(self, rows: list[Mapping[str, Any]]) -> str:
        """Extract key insights from medium datasets."""
        if not rows:
            return ""
        
        # Find the main metric column
        main_metric = None
        main_values = []
        
        if rows:
            first_row = rows[0]
            for k, v in first_row.items():
                if isinstance(v, (int, float)) and v > 0:
                    main_metric = k
                    break
        
        if main_metric:
            main_values = [row.get(main_metric, 0) for row in rows if isinstance(row.get(main_metric), (int, float))]
        
        if not main_values:
            return f"\n\nAnálise de {len(rows)} registros"
        
        # Calculate key statistics
        total = sum(main_values)
        avg = total / len(main_values)
        max_val = max(main_values)
        min_val = min(main_values)
        
        text_parts = [f"\n\nPrincipais insights ({len(rows)} registros):"]
        text_parts.append(f"  Total: {total:,.0f}")
        text_parts.append(f"  Média: {avg:,.2f}")
        text_parts.append(f"  Máximo: {max_val:,.0f}")
        text_parts.append(f"  Mínimo: {min_val:,.0f}")
        
        return "\n".join(text_parts)
    
    def _detect_patterns_and_insights(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Detect patterns and provide intelligent insights.
        
        Args:
            rows: List of data rows to analyze for patterns.
            user_query: Original user query for context.
            
        Returns:
            String containing detected insights with emojis and formatting,
            or empty string if no patterns detected.
        """
        if not rows:
            return ""
        
        insights = []
        
        # Pattern 1: 1:1 ratio detection (clientes = compras)
        if self._detect_one_to_one_ratio(rows):
            insights.append("Insight: Cada cliente fez exatamente uma compra (relação 1:1 entre clientes e compras)")
        
        # Pattern 2: Dominance detection (one state/category dominates)
        dominance_insight = self._detect_dominance_pattern(rows)
        if dominance_insight:
            insights.append(f"Insight: {dominance_insight}")
        
        # Pattern 3: Geographic concentration
        geo_insight = self._detect_geographic_concentration(rows)
        if geo_insight:
            insights.append(f"Insight: {geo_insight}")
        
        # Pattern 4: Temporal patterns
        temporal_insight = self._detect_temporal_patterns(rows)
        if temporal_insight:
            insights.append(f"Insight: {temporal_insight}")
        
        # Pattern 5: Category concentration
        category_insight = self._detect_category_concentration(rows)
        if category_insight:
            insights.append(f"Insight: {category_insight}")
        
        if insights:
            return "\n\n" + "\n".join(insights)
        
        return ""
    
    def _detect_one_to_one_ratio(self, rows: list[Mapping[str, Any]]) -> bool:
        """Detect if there's a 1:1 ratio between two metrics.
        
        Analyzes numeric columns in the dataset to identify if any two columns
        maintain a perfect 1:1 ratio across all rows (e.g., clientes = compras).
        
        Args:
            rows: List of data rows to analyze for 1:1 ratio patterns.
            
        Returns:
            True if a 1:1 ratio is detected between any two numeric columns,
            False otherwise.
        """
        if len(rows) < 2:
            return False
        
        # Look for two numeric columns that might be in 1:1 ratio
        numeric_columns = []
        for k, v in rows[0].items():
            if isinstance(v, (int, float)) and k not in ['period', 'month', 'year']:
                numeric_columns.append(k)
        
        if len(numeric_columns) < 2:
            return False
        
        # Check if any two columns have 1:1 ratio
        for i, col1 in enumerate(numeric_columns):
            for col2 in numeric_columns[i+1:]:
                ratios = []
                for row in rows:
                    val1 = row.get(col1, 0)
                    val2 = row.get(col2, 0)
                    if val1 > 0 and val2 > 0:
                        ratios.append(val1 / val2)
                
                if ratios and all(abs(r - 1.0) < 0.01 for r in ratios):  # Within 1% tolerance
                    return True
        
        return False
    
    def _detect_dominance_pattern(self, rows: list[Mapping[str, Any]]) -> str:
        """Detect if one item dominates the dataset.
        
        Analyzes the dataset to identify if any single item (state, category, etc.)
        represents a significant portion (>40%) of the total metric value.
        
        Args:
            rows: List of data rows to analyze for dominance patterns.
            
        Returns:
            String describing the dominant item and its percentage,
            or empty string if no dominance detected.
        """
        if len(rows) < 3:
            return ""
        
        # Find the main metric column
        main_metric = None
        for k, v in rows[0].items():
            if isinstance(v, (int, float)) and k not in ['period', 'month', 'year']:
                main_metric = k
                break
        
        if not main_metric:
            return ""
        
        # Calculate total and find dominance
        total = sum(row.get(main_metric, 0) for row in rows)
        if total == 0:
            return ""
        
        # Find the top item
        top_item = max(rows, key=lambda x: x.get(main_metric, 0))
        top_value = top_item.get(main_metric, 0)
        top_percentage = (top_value / total) * 100
        
        # Get the key identifier (state, category, etc.)
        identifier_col = None
        for k, v in top_item.items():
            if k != main_metric and not isinstance(v, (int, float)):
                identifier_col = k
                break
        
        if identifier_col and top_percentage > 40:  # Dominance threshold
            identifier = top_item.get(identifier_col, 'Unknown')
            return f"{identifier} domina com {top_percentage:.1f}% do total"
        
        return ""
    
    def _detect_geographic_concentration(self, rows: list[Mapping[str, Any]]) -> str:
        """Detect geographic concentration patterns.
        
        Analyzes the dataset to identify if there's high geographic concentration
        where the top 3 states represent more than 70% of the total metric value.
        
        Args:
            rows: List of data rows to analyze for geographic concentration.
            
        Returns:
            String describing the geographic concentration pattern,
            or empty string if no high concentration detected.
        """
        if len(rows) < 3:
            return ""
        
        # Look for state column
        state_col = None
        for k, v in rows[0].items():
            if 'state' in k.lower() and not isinstance(v, (int, float)):
                state_col = k
                break
        
        if not state_col:
            return ""
        
        # Find the main metric
        main_metric = None
        for k, v in rows[0].items():
            if isinstance(v, (int, float)) and k not in ['period', 'month', 'year']:
                main_metric = k
                break
        
        if not main_metric:
            return ""
        
        # Calculate concentration in top 3 states
        total = sum(row.get(main_metric, 0) for row in rows)
        if total == 0:
            return ""
        
        # Sort by metric value
        sorted_rows = sorted(rows, key=lambda x: x.get(main_metric, 0), reverse=True)
        top3_total = sum(row.get(main_metric, 0) for row in sorted_rows[:3])
        top3_percentage = (top3_total / total) * 100
        
        if top3_percentage > 70:  # High concentration threshold
            top3_states = [row.get(state_col, 'Unknown') for row in sorted_rows[:3]]
            return f"Alta concentração geográfica: {', '.join(top3_states)} representam {top3_percentage:.1f}% do total"
        
        return ""
    
    def _detect_temporal_patterns(self, rows: list[Mapping[str, Any]]) -> str:
        """Detect temporal patterns in the data.
        
        Analyzes the dataset to identify temporal trends such as growth or decline
        patterns over time periods.
        
        Args:
            rows: List of data rows to analyze for temporal patterns.
            
        Returns:
            String describing the temporal trend detected,
            or empty string if no clear pattern found.
        """
        if len(rows) < 3:
            return ""
        
        # Look for temporal columns
        temporal_col = None
        for k, v in rows[0].items():
            if any(temporal in k.lower() for temporal in ['period', 'month', 'year', 'date']):
                temporal_col = k
                break
        
        if not temporal_col:
            return ""
        
        # Find the main metric
        main_metric = None
        for k, v in rows[0].items():
            if isinstance(v, (int, float)) and k != temporal_col:
                main_metric = k
                break
        
        if not main_metric:
            return ""
        
        # Check for growth/decline pattern
        sorted_rows = sorted(rows, key=lambda x: str(x.get(temporal_col, '')))
        values = [row.get(main_metric, 0) for row in sorted_rows]
        
        if len(values) >= 3:
            # Simple trend detection
            first_half = sum(values[:len(values)//2])
            second_half = sum(values[len(values)//2:])
            
            if second_half > first_half * 1.2:  # 20% growth
                return "Tendência de crescimento ao longo do período analisado"
            elif first_half > second_half * 1.2:  # 20% decline
                return "Tendência de declínio ao longo do período analisado"
        
        return ""
    
    def _detect_category_concentration(self, rows: list[Mapping[str, Any]]) -> str:
        """Detect category concentration patterns.
        
        Analyzes the dataset to identify if there's high concentration in a single
        category that represents more than 50% of the total metric value.
        
        Args:
            rows: List of data rows to analyze for category concentration.
            
        Returns:
            String describing the category concentration pattern,
            or empty string if no high concentration detected.
        """
        if len(rows) < 3:
            return ""
        
        # Look for category column
        category_col = None
        for k, v in rows[0].items():
            if 'category' in k.lower() and not isinstance(v, (int, float)):
                category_col = k
                break
        
        if not category_col:
            return ""
        
        # Find the main metric
        main_metric = None
        for k, v in rows[0].items():
            if isinstance(v, (int, float)) and k != category_col:
                main_metric = k
                break
        
        if not main_metric:
            return ""
        
        # Calculate concentration in top category
        total = sum(row.get(main_metric, 0) for row in rows)
        if total == 0:
            return ""
        
        top_category = max(rows, key=lambda x: x.get(main_metric, 0))
        top_value = top_category.get(main_metric, 0)
        top_percentage = (top_value / total) * 100
        
        if top_percentage > 50:  # High category concentration
            category_name = top_category.get(category_col, 'Unknown')
            return f"Alta concentração em {category_name} ({top_percentage:.1f}% do total)"
        
        return ""
    
    def _format_penetration_data(self, rows: list[Mapping[str, Any]]) -> str:
        """Format penetration data by state and category."""
        from collections import defaultdict
        
        # Group by state
        state_data = defaultdict(dict)
        for row in rows:
            state = row.get('state', 'Unknown')
            category = row.get('category', 'Unknown')
            penetration = row.get('penetration', 0)
            
            # Skip None values
            if state is None or category is None:
                continue
                
            state_data[state][category] = penetration
        
        # Use more efficient string building
        text_parts = ["\n\nPenetração por estado:"]
        for state in sorted(state_data.keys()):
            categories = state_data[state]
            # Filter out None values and sort safely
            category_parts = []
            for cat, val in categories.items():
                if cat is not None and val is not None:
                    category_parts.append(f"{cat}: {val}")
            
            if category_parts:
                category_parts.sort()  # Sort the list instead of using sorted() on dict items
                text_parts.append(f"{state}: {', '.join(category_parts)}")
        
        return "\n".join(text_parts)
    
    def _format_state_data(self, rows: list[Mapping[str, Any]]) -> str:
        """Format data grouped by state."""
        text_parts = ["\n\nDados por estado:"]
        for row in rows:
            state = row.get('state', 'Unknown')
            if state is None:
                continue
                
            values = []
            for k, v in row.items():
                if k != 'state' and v is not None:
                    if isinstance(v, (int, float)) and v > 1000:
                        values.append(f"{k}: {v:,.0f}")
                    else:
                        values.append(f"{k}: {v}")
            if values:
                text_parts.append(f"{state}: {', '.join(values)}")
        
        return "\n".join(text_parts)
    
    def _format_category_data(self, rows: list[Mapping[str, Any]]) -> str:
        """Format data grouped by category."""
        text_parts = ["\n\nDados por categoria:"]
        for row in rows:
            category = row.get('category', 'Unknown')
            if category is None:
                continue
                
            values = []
            for k, v in row.items():
                if k != 'category' and v is not None:
                    if isinstance(v, (int, float)) and v > 1000:
                        values.append(f"{k}: {v:,.0f}")
                    else:
                        values.append(f"{k}: {v}")
            if values:
                text_parts.append(f"{category}: {', '.join(values)}")
        
        return "\n".join(text_parts)
    
    def _fallback_normalize(
        self, 
        user_query: str, 
        plan: _PlanView, 
        result: _ResultView
    ) -> dict[str, Any]:
        """Simple fallback normalization when LLM fails."""
        
        # Let LLM handle ALL formatting - no hardcoded messages
        # Just provide basic data structure for LLM to work with
        text = f"Encontrados {result.row_count} registros."
        
        # Use the same LLM-based decision logic
        needs_complete_data = self._should_show_complete_data(user_query, result)
        
        if needs_complete_data and result.rows:
            # Show all data for complete analysis
            text += self._format_complete_data(result.rows, user_query)
        elif result.rows:
            # Use intelligent formatting for other cases
            text += self._format_all_data(result.rows, user_query)
        
        return {
            "text": text,
            "meta": {
                "sql": plan.sql,
                "row_count": result.row_count,
                "limit_applied": result.limit_applied,
                "exec_ms": result.exec_ms,
                "fallback_used": True
            }
        }


# Helper functions
def _as_plan(plan: Mapping[str, Any] | _PlanView) -> _PlanView:
    """Convert plan to _PlanView."""
    if isinstance(plan, _PlanView):
        return plan
    return _PlanView(
        sql=plan.get("sql", ""),
        limit_applied=plan.get("limit_applied", False),
    )


def _as_result(result: Mapping[str, Any] | _ResultView) -> _ResultView:
    """Convert result to _ResultView."""
    if isinstance(result, _ResultView):
        return result
    return _ResultView(
        rows=result.get("rows", []),
        row_count=result.get("row_count", 0),
        exec_ms=result.get("exec_ms", 0.0),
        limit_applied=result.get("limit_applied", False),
    )


def _coerce_answer(payload: dict[str, Any]) -> Any:
    """Convert payload to Answer if available, else return dict."""
    try:
        from app.contracts.answer import Answer
        return Answer.from_dict(payload)
    except Exception:
        return payload

