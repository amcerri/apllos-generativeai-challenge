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

import math
import re
import json
import os
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
    from app.config import get_config
except Exception:  # pragma: no cover - optional
    def get_config():
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
        """Load the system prompt from file."""
        try:
            prompt_path = Path(__file__).parent.parent.parent / "prompts" / "analytics" / "normalizer_system.txt"
            return prompt_path.read_text(encoding="utf-8")
        except Exception:
            return ""
    
    def _load_examples(self) -> list[dict[str, Any]]:
        """Load few-shot examples from JSONL file."""
        try:
            examples_path = Path(__file__).parent.parent.parent / "prompts" / "analytics" / "normalizer_examples.jsonl"
            examples = []
            for line in examples_path.read_text(encoding="utf-8").strip().split('\n'):
                if line.strip():
                    examples.append(json.loads(line))
            return examples
        except Exception:
            return []


    def normalize(
        self,
        *,
        plan: Mapping[str, Any] | _PlanView,
        result: Mapping[str, Any] | _ResultView,
        question: str | None = None,
    ) -> Any:
        """Normalize using LLM-powered approach with fallback."""
        
        # Convert inputs to standard format
        plan_view = _as_plan(plan)
        result_view = _as_result(result)
        user_query = question or "Consulta de dados"
        
        # For penetration queries with large datasets, use fallback directly
        if (result_view.row_count > 500 and 
            ('penetração' in user_query.lower() or 'penetration' in user_query.lower()) and
            result_view.rows and 
            'state' in result_view.rows[0] and 'category' in result_view.rows[0]):
            self.log.info("Using fallback for large penetration query")
            return self._fallback_normalize(user_query, plan_view, result_view)
        
        # Try LLM-powered normalization with fallback
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
        """Use LLM to normalize the results."""
        
        try:
            from openai import OpenAI
        except ImportError:
            return None
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        
        # Get configuration
        config = get_config()
        if config is None:
            # Fallback to hardcoded values if config not available
            model = "gpt-4o-mini"
            max_tokens = 800
            temperature = 0.1
            timeout = 10.0
            max_examples = 1
        else:
            model = config.get_llm_model("analytics_normalizer")
            max_tokens = config.get_llm_max_tokens("analytics_normalizer")
            temperature = config.get_llm_temperature("analytics_normalizer")
            timeout = config.get_llm_timeout("analytics_normalizer")
            max_examples = config.get("analytics.normalizer.max_examples_in_prompt", 1)
        
        client = OpenAI(api_key=api_key)
        
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
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
        except Exception as e:
            # Silently fail for LLM API issues
            return None
        
        # Parse response
        response_text = response.choices[0].message.content.strip()
        try:
            response_data = json.loads(response_text)
            
            # For large datasets, append all data after LLM analysis
            if input_data.get("has_more_data", False) and result.rows:
                if "text" in response_data:
                    response_data["text"] += self._format_all_data(result.rows, user_query)
            
            return response_data
        except json.JSONDecodeError:
            # Try to extract JSON from response if enabled in config
            if config and config.get("analytics.normalizer.json_extraction_regex", True):
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    response_data = json.loads(json_match.group())
                    # For large datasets, append all data after LLM analysis
                    if input_data.get("has_more_data", False) and result.rows:
                        if "text" in response_data:
                            response_data["text"] += self._format_all_data(result.rows, user_query)
                    return response_data
            return None
    
    def _format_all_data(self, rows: list[Mapping[str, Any]], user_query: str) -> str:
        """Format all data for large datasets."""
        if not rows:
            return ""
        
        # For very large datasets, limit the display to prevent timeout
        max_display = 2000  # Increased limit for penetration queries
        if len(rows) > max_display:
            rows = rows[:max_display]
            truncated = True
        else:
            truncated = False
        
        # Check if this is a penetration query (state + category)
        if len(rows) > 0:
            first_row = rows[0]
            if 'state' in first_row and 'category' in first_row:
                result = self._format_penetration_data(rows)
                if truncated:
                    result += f"\n\n(Exibindo {max_display} de {len(rows)} registros)"
                return result
            elif 'state' in first_row:
                result = self._format_state_data(rows)
                if truncated:
                    result += f"\n\n(Exibindo {max_display} de {len(rows)} registros)"
                return result
            elif 'category' in first_row:
                result = self._format_category_data(rows)
                if truncated:
                    result += f"\n\n(Exibindo {max_display} de {len(rows)} registros)"
                return result
        
        # Generic formatting for other queries
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
        
        if truncated:
            text_parts.append(f"\n(Exibindo {max_display} de {len(rows)} registros)")
        
        return "\n".join(text_parts)
    
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
        
        # Basic formatting for common cases
        if result.row_count == 0:
            text = f"Nenhum resultado encontrado para a consulta: {user_query}"
        elif result.row_count == 1 and len(result.rows) == 1:
            # Single row result
            row = result.rows[0]
            if len(row) == 1:
                # Single value
                value = list(row.values())[0]
                if isinstance(value, (int, float)):
                    if value > 1000:
                        text = f"O resultado é {value:,.0f}."
                    else:
                        text = f"O resultado é {value}."
                else:
                    text = f"O resultado é {value}."
            else:
                # Multiple columns in single row
                text = f"Resultado encontrado com {len(row)} campos."
        else:
            # Multiple rows
            text = f"Encontrados {result.row_count} registros."
            
            # Show all data for any size dataset
            if result.rows:
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

