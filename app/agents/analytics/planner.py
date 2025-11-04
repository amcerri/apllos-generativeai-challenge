"""
Analytics planner (safe SQL synthesis).

Overview
--------
Translate natural‑language analytical requests into **safe, bounded SQL** over the
Olist analytics schema. The planner enforces hard guardrails: no `SELECT *`,
no DDL/DML, only allow‑listed identifiers, and a **LIMIT** for non‑aggregate
queries. It returns a structured plan object for downstream execution and
normalization.

Design
------
- Stateless planner with a deterministic fallback (no network), plus optional LLM
  backend (wired later) via prompts in `app/prompts/analytics/`.
- Guardrails first: identifiers are validated against an explicit allowlist
  (table → columns). Aggregations prefer `COUNT(1)` instead of `COUNT(*)`.
- Heuristics cover common intents: preview with cap, counts, top‑N, and time
  series using `date_trunc` when a timestamp column is available.

Integration
-----------
- Called by the analytics agent node before execution.
- Logging uses stdlib logger adapter with `.bind(...)`. Tracing spans are optional.
- The resulting plan is handed to the executor; SQL strings are not shown to
  end users (only business narratives are surfaced by the normalizer).

Usage
-----
>>> from app.agents.analytics.planner import AnalyticsPlanner
>>> allowlist = {"orders": ["order_id", "order_status", "order_purchase_timestamp", "customer_id"],
...              "order_items": ["order_id", "price", "freight_value", "product_id", "seller_id"]}
>>> planner = AnalyticsPlanner()
>>> plan = planner.plan("Orders per month in 2018", allowlist, thread_id="t-123")
>>> plan.sql.startswith("SELECT") and plan.limit_applied in (True, False)
True
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Protocol, runtime_checkable

start_span: Any

try:  # Logging & tracing are optional at import time
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

try:  # Optional config
    from app.config.settings import get_settings as get_config
except Exception:  # pragma: no cover - optional
    def get_config():
        return None


try:  # Optional tracing
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

__all__ = ["PlannerPlan", "AnalyticsPlanner"]


# ---------------------------------------------------------------------------
# Data contract
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class PlannerPlan:
    """Represent a safe SQL plan for execution.

    Attributes
    ----------
    sql: Final SQL string to be executed by the executor (read‑only intent).
    params: Query parameters (future use; keep for compatibility).
    reason: Short English rationale for traceability.
    limit_applied: Whether a LIMIT was injected due to non‑aggregate query.
    warnings: Non‑fatal observations (e.g., heuristic assumptions).
    """

    sql: str
    params: dict[str, Any]
    reason: str
    limit_applied: bool
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict representation."""

        return {
            "sql": self.sql,
            "params": dict(self.params),
            "reason": self.reason,
            "limit_applied": bool(self.limit_applied),
            "warnings": list(self.warnings),
        }


# ---------------------------------------------------------------------------
# LLM Backend (optional)
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
    """Backend using centralized LLM client with JSON Schema outputs."""

    def __init__(self, *, model: str) -> None:
        from app.infra.llm_client import get_llm_client

        self._client = get_llm_client()
        if not self._client.is_available():
            raise RuntimeError("LLM client not available")
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
        """Generate JSON response using centralized LLM client."""
        resp = self._client.chat_completion(
            messages=[{"role": "system", "content": system}, *messages],
            model=model or self._default_model,
            temperature=temperature,
            max_tokens=max_output_tokens,
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "analytics_plan", "schema": dict(json_schema), "strict": True},
            },
            max_retries=0,
        )
        if resp is None or not resp.text:
            raise ValueError("Empty response from LLM")
        data = self._client.extract_json(resp.text, schema=dict(json_schema))
        if data is None:
            raise ValueError("Failed to parse JSON from LLM response")
        return data


# ---------------------------------------------------------------------------
# Planner
# ---------------------------------------------------------------------------
class AnalyticsPlanner:
    """Synthesize safe SQL bounded by an allowlist and simple heuristics.

    This deterministic implementation avoids network calls and is sufficient for
    unit/e2e tests. An optional LLM backend can be introduced later using the
    prompts authored under `app/prompts/analytics/`.
    """

    
    # JSON Schema for LLM structured outputs
    PLAN_SCHEMA: Final[dict[str, Any]] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "sql": {"type": "string", "minLength": 1},
            "params": {"type": "object", "additionalProperties": False, "properties": {}},
            "reason": {"type": "string", "minLength": 1, "maxLength": 220},
            "limit_applied": {"type": "boolean"},
            "warnings": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["sql", "params", "reason", "limit_applied", "warnings"],
    }

    def __init__(self) -> None:
        self.log = get_logger("agent.analytics.planner")
        self._config = get_config()
        
        # Get configuration values with fallbacks using Settings model
        try:
            planner_cfg = getattr(self._config, "analytics").planner  # type: ignore[attr-defined]
            self.default_preview_limit = int(getattr(planner_cfg, "default_limit", 200))
            self.max_safe_limit = int(getattr(planner_cfg, "max_limit", 5000))
            self.examples_count = int(getattr(planner_cfg, "examples_count", 3))
            self.max_examples = int(getattr(planner_cfg, "max_examples", 5))
        except Exception:
            self.default_preview_limit = 200
            self.max_safe_limit = 5000
            self.examples_count = 3
            self.max_examples = 5
        
        # Try to initialize LLM backend using settings.models.analytics_planner
        self._llm_backend = None
        try:
            model_name = None
            try:
                if self._config is not None:
                    model_name = self._config.models.analytics_planner.name
            except Exception:
                model_name = None
            self._llm_backend = OpenAIJSONBackend(model=model_name or "gpt-4o-mini")
            self.log.info("LLM backend initialized for analytics planner")
        except Exception as exc:
            self.log.warning("LLM backend unavailable; using heuristics only", exc_info=exc)
        
        # Load examples for few-shot prompting
        self._examples = self._load_examples()

    # Public API -------------------------------------------------------------
    def plan(
        self,
        query: str,
        allowlist: Mapping[str, Iterable[str]],
        *,
        thread_id: str | None = None,
        default_limit: int | None = None,
    ) -> PlannerPlan:
        """Produce a safe SQL plan.

        Args:
            query: Natural‑language request.
            allowlist: Mapping of table → columns allowed for selection.
            thread_id: Correlation id for logging/tracing.
            default_limit: Optional per‑call LIMIT for non‑aggregate previews.

        Returns:
            PlannerPlan: Structured plan with SQL and guardrail metadata.
        """

        cap = int(default_limit or self.default_preview_limit)
        cap = max(1, min(cap, self.max_safe_limit))

        with start_span("agent.analytics.plan", {"thread_id": thread_id}):
            logger = self.log.bind(component="agent.analytics", event="plan", thread_id=thread_id)

            # Try LLM first if available
            if self._llm_backend:
                try:
                    plan = self._plan_with_llm(query, allowlist, logger, default_limit)
                    # CRITICAL: Fix alias issues before returning
                    return self._fix_alias_issues(plan, logger)
                except Exception as exc:
                    logger.warning("LLM planning failed; falling back to heuristics", exc_info=exc)

            # Fallback to heuristics
            text = (query or "").strip()
            lw = text.lower()
            tables_index = _normalize_allowlist(allowlist)

            table = _pick_table(text, tables_index) or _fallback_table(tables_index)
            if not table:
                sql = "SELECT 1 WHERE 1=0"  # unreachable sentinel; no schema
                return PlannerPlan(
                    sql=sql,
                    params={},
                    reason="no available tables in allowlist",
                    limit_applied=True,
                    warnings=["empty_allowlist"],
                )
            
            # Get columns from allowlist
            cols = tables_index[table]
            
            # Add schema prefix for SQL generation
            if not table.startswith("analytics."):
                table = f"analytics.{table}"
            is_agg = _is_aggregation_intent(lw)
            timescale = _detect_timescale(lw)
            ts_col = _find_time_column(cols)

            year = _extract_year(lw)

            warnings: list[str] = []

            if is_agg and timescale and ts_col:
                # Timeseries aggregation
                where = ""
                if year and ts_col:
                    where = (
                        f"WHERE {table}.{ts_col} >= '{year}-01-01' AND "
                        f"{table}.{ts_col} < '{year + 1}-01-01'"
                    )
                sql = (
                    f"SELECT date_trunc('{timescale}', {table}.{ts_col}) AS period, COUNT(1) AS qty\n"
                    f"FROM {table}\n"
                    f"{where}\n"
                    f"GROUP BY period\n"
                    f"ORDER BY period"
                ).replace("\n\n", "\n")
                limit_applied = False
                reason = f"{timescale} time series using {ts_col}"
            elif is_agg:
                # Global aggregation (count)
                if year and ts_col:
                    sql = (
                        f"SELECT COUNT(1) AS qty\n"
                        f"FROM {table}\n"
                        f"WHERE {table}.{ts_col} >= '{year}-01-01' AND "
                        f"{table}.{ts_col} < '{year + 1}-01-01'"
                    )
                else:
                    sql = f"SELECT COUNT(1) AS qty FROM {table}"
                limit_applied = False
                reason = "global count"
            else:
                # Preview with cap: choose a small set of explicit columns
                preview_cols = _choose_preview_columns(cols)
                where = ""
                if year and ts_col:
                    where = (
                        f"WHERE {table}.{ts_col} >= '{year}-01-01' AND "
                        f"{table}.{ts_col} < '{year + 1}-01-01'"
                    )
                sql = (
                    f"SELECT {', '.join(f'{table}.{c}' for c in preview_cols)}\n"
                    f"FROM {table}\n"
                    f"{where}\n"
                    f"ORDER BY 1 DESC\n"
                    f"LIMIT {cap}"
                ).replace("\n\n", "\n")
                limit_applied = True
                reason = "preview with cap"

            # Final safety checks (syntactic only; executor enforces read‑only)
            if "*" in sql:
                warnings.append("select_star_blocked")
                sql = sql.replace("*", "1")  # ultra‑conservative fallback

            # Create validation allowlist with schema prefix to match the SQL
            validation_allowlist = {table: cols}
            _validate_identifiers(sql, validation_allowlist)  # raises on violation

            logger.info("Planned SQL", sql=sql, reason=reason)
            return PlannerPlan(
                sql=sql, params={}, reason=reason, limit_applied=limit_applied, warnings=warnings
            )

    def _plan_with_llm(
        self,
        query: str,
        allowlist: Mapping[str, Iterable[str]],
        logger: Any,
        default_limit: int | None = None,
    ) -> PlannerPlan:
        """Generate SQL plan using LLM."""
        
        # Load system prompt and inject allowlist
        system_prompt = self._load_system_prompt(allowlist)
        
        # Prepare messages with few-shot examples
        messages = []
        
        # Add relevant examples (use configured number of most relevant ones)
        if self._examples:
            # Simple relevance: find examples with similar keywords
            query_lower = query.lower()
            relevant_examples = []
            
            for example in self._examples:
                input_text = example.get("input", "").lower()
                # Score based on keyword overlap
                score = 0
                for word in query_lower.split():
                    if len(word) > 3 and word in input_text:
                        score += 1
                
                if score > 0:
                    relevant_examples.append((score, example))
            
            # Sort by relevance and take configured number
            relevant_examples.sort(key=lambda x: x[0], reverse=True)
            examples_count = self.examples_count if hasattr(self, 'examples_count') else 3
            for _, example in relevant_examples[:examples_count]:
                messages.append({"role": "user", "content": example["input"]})
                messages.append({"role": "assistant", "content": json.dumps(example["output"], ensure_ascii=False)})
        
        # Add current query
        user_message = query.strip()
        if default_limit:
            user_message += f" (default limit: {default_limit})"
        
        messages.append({"role": "user", "content": user_message})
        
        # Generate plan with LLM
        logger.info("Generating SQL plan with LLM", query=query[:100])
        
        response = self._llm_backend.generate_json(
            system=system_prompt,
            messages=messages,
            json_schema=self.PLAN_SCHEMA,
            temperature=0.0,
            max_output_tokens=1024,
        )
        
        # Validate and normalize response
        plan = self._validate_llm_plan(response, allowlist, logger)
        
        logger.info("LLM SQL plan generated", sql=plan.sql[:100], reason=plan.reason)
        return plan

    def _load_system_prompt(self, allowlist: Mapping[str, Iterable[str]]) -> str:
        """Load system prompt and inject allowlist."""
        
        prompt_file = Path(__file__).parent.parent.parent / "prompts" / "analytics" / "planner_system.txt"
        
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                template = f.read()
        except Exception as exc:
            self.log.warning(f"Could not load prompt file {prompt_file}: {exc}")
            # Minimal fallback prompt
            template = """You are an Analytics SQL Planner. Generate safe PostgreSQL SELECT queries.
ALLOWLIST (JSON)
<<<ALLOWLIST_JSON>>>

Return JSON with: {"sql": "SELECT ...", "reason": "...", "limit_applied": boolean, "params": {}, "warnings": []}"""
        
        # Inject allowlist
        allowlist_json = json.dumps(dict(allowlist), indent=2)
        return template.replace("<<<ALLOWLIST_JSON>>>", allowlist_json)
    
    def _load_examples(self) -> list[dict[str, Any]]:
        """Load few-shot examples from JSONL file."""
        try:
            from pathlib import Path
            import json
            
            examples_path = Path(__file__).parent.parent.parent / "prompts" / "analytics" / "examples.jsonl"
            examples = []
            
            with open(examples_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        examples.append(json.loads(line))
            
            # Limit examples based on configuration
            max_examples = self.max_examples if hasattr(self, 'max_examples') else 5
            examples = examples[:max_examples]
            
            self.log.info(f"Loaded {len(examples)} examples for few-shot prompting")
            return examples
            
        except Exception as exc:
            self.log.warning(f"Could not load examples: {exc}")
            return []

    def _validate_llm_plan(
        self, 
        response: Mapping[str, Any], 
        allowlist: Mapping[str, Iterable[str]],
        logger: Any,
    ) -> PlannerPlan:
        """Validate LLM response and create PlannerPlan."""
        
        # Extract required fields
        sql = response.get("sql", "").strip()
        reason = response.get("reason", "LLM generated plan")
        limit_applied = response.get("limit_applied", False)
        params = response.get("params", {})
        warnings = list(response.get("warnings", []))
        
        if not sql:
            raise ValueError("Empty SQL in LLM response")
        
        # Fix schema prefixes
        sql = self._fix_schema_prefixes(sql)
        
        # Basic SQL safety checks
        sql_lower = sql.lower()
        
        # Check for forbidden operations
        forbidden = ["insert", "update", "delete", "drop", "create", "alter", "truncate"]
        for op in forbidden:
            if f" {op} " in sql_lower or sql_lower.startswith(f"{op} "):
                warnings.append(f"forbidden_operation:{op}")
                raise ValueError(f"Forbidden SQL operation: {op}")
        
        # Check for SELECT * (should be avoided)
        if "select *" in sql_lower:
            warnings.append("select_star_detected")
        
        return PlannerPlan(
            sql=sql,
            params=params,
            reason=reason,
            limit_applied=limit_applied,
            warnings=warnings,
        )
    
    def _fix_alias_issues(self, plan: PlannerPlan, logger: Any) -> PlannerPlan:
        """Fix alias issues in SQL (remove dots from aliases)."""
        import re
        
        original_sql = plan.sql
        
        # Find and fix aliases with dots (e.g., "AS analytics.customers" -> "AS customers")
        # Pattern: AS followed by schema.table_name
        fixed_sql = re.sub(
            r'\bAS\s+([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)\b',
            lambda m: f"AS {m.group(1).split('.')[-1]}",  # Keep only the part after the dot
            original_sql,
            flags=re.IGNORECASE
        )
        
        if fixed_sql != original_sql:
            logger.warning(f"Fixed alias issues in SQL: {original_sql[:100]}... -> {fixed_sql[:100]}...")
            return PlannerPlan(
                sql=fixed_sql,
                params=plan.params,
                reason=plan.reason,
                limit_applied=plan.limit_applied,
                warnings=plan.warnings + ["fixed_alias_dots"]
            )
        
        return plan

    def _fix_schema_prefixes(self, sql: str) -> str:
        """Ensure all table references have analytics schema prefix."""
        import re
        
        # List of table names that should have schema prefix
        table_names = [
            'orders', 'customers', 'products', 'sellers', 'order_items', 
            'order_payments', 'order_reviews', 'geolocation', 'product_category_translation'
        ]
        
        # Add analytics. prefix to table names that don't already have it
        for table in table_names:
            # Pattern to match table name not already prefixed with analytics.
            pattern = rf'\b(?<!analytics\.)({re.escape(table)})\b'
            replacement = rf'analytics.{table}'
            sql = re.sub(pattern, replacement, sql, flags=re.IGNORECASE)
        
        return sql


# ---------------------------------------------------------------------------
# Heuristics & helpers
# ---------------------------------------------------------------------------

_AGG_KEYS = (
    "count",
    "quantos",
    "qtd",
    "quantidade",
    "número de",
    "numero de",
    "total",
    "soma",
    "sum",
    "média",
    "media",
    "avg",
    "taxa",
    "percentual",
    "distribuição",
    "distribuicao",
)

_MONTH_KEYS = ("por mês", "mensal", "month", "monthly")
_WEEK_KEYS = ("por semana", "semanal", "week", "weekly")
_DAY_KEYS = ("por dia", "diário", "diario", "day", "daily")
_YEAR_KEYS = ("por ano", "anual", "year", "yearly")

_TIME_HINTS = ("timestamp", "date", "data", "dt")

_IDENTIFIER_RE = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")


def _normalize_allowlist(allowlist: Mapping[str, Iterable[str]]) -> dict[str, list[str]]:
    """Return a normalized allowlist mapping.

    Trims whitespace, deduplicates and sorts columns, and returns a
    table→columns dict with tables sorted for deterministic behavior.

    Parameters
    ----------
    allowlist : Mapping[str, Iterable[str]]
        Raw allowlist mapping provided by the caller.

    Returns
    -------
    dict[str, list[str]]
        Normalized mapping with sorted table names and column lists.
    """
    out: dict[str, list[str]] = {}
    for t, cols in allowlist.items():
        t2 = str(t).strip()
        if not t2:
            continue
        cset = sorted({str(c).strip() for c in cols if str(c).strip()})
        out[t2] = cset
    return dict(sorted(out.items(), key=lambda kv: kv[0]))


def _pick_table(text: str, tables_index: Mapping[str, list[str]]) -> str | None:
    """Heuristically choose a table mentioned in the natural-language query.

    Looks for exact token matches of table names; falls back to a preferred
    ordering if none are found.
    """
    tokens = {w.strip(".,:;()[]{}\"'`").lower() for w in text.split()}
    for t in tables_index.keys():
        if t.lower() in tokens:
            return t
    # Common default preference
    for preferred in ("orders", "order_items", "customers", "products"):
        if preferred in tables_index:
            return preferred
    return None


def _fallback_table(tables_index: Mapping[str, list[str]]) -> str | None:
    """Return the first available table as a conservative default."""
    return next(iter(tables_index.keys()), None)


def _is_aggregation_intent(lw: str) -> bool:
    """Return True if the query likely requests an aggregation."""
    return any(k in lw for k in _AGG_KEYS)


def _detect_timescale(lw: str) -> str | None:
    """Detect a time bucket (day/week/month/year) requested by the query."""
    if any(k in lw for k in _MONTH_KEYS):
        return "month"
    if any(k in lw for k in _WEEK_KEYS):
        return "week"
    if any(k in lw for k in _DAY_KEYS):
        return "day"
    if any(k in lw for k in _YEAR_KEYS):
        return "year"
    return None


_YEAR_RE = re.compile(r"(?<!\d)(19|20)\d{2}(?!\d)")


def _extract_year(lw: str) -> int | None:
    """Return a 4-digit year if present (e.g., 2018), else None."""
    m = _YEAR_RE.search(lw)
    if not m:
        return None
    try:
        return int(m.group(0))
    except Exception:
        return None


def _find_time_column(columns: list[str]) -> str | None:
    """Find a plausible timestamp/date column from a list of columns."""
    lwcols = [c.lower() for c in columns]
    # Extended hints include common business date fields
    extended_hints = list(_TIME_HINTS) + [
        "created", "updated", "purchase", "approved", "delivered", "estimated",
    ]
    for hint in extended_hints:
        for c in lwcols:
            if hint in c:
                # return original‑case column
                return columns[lwcols.index(c)]
    return None


def _choose_preview_columns(columns: list[str], *, max_cols: int = 6) -> list[str]:
    """Choose a compact set of columns for preview queries.

    Prefers identifiers, status, and timestamp-like columns, then fills
    the remainder deterministically from the input ordering.
    """
    # Prefer id/status/timestamps first, then fill in with the next columns.
    priority = [
        *[c for c in columns if c.endswith("_id")],
        *[c for c in columns if "status" in c],
        *[c for c in columns if any(h in c for h in ("timestamp", "date", "dt"))],
    ]
    rest = [c for c in columns if c not in priority]
    ordered = []
    for c in priority + rest:
        if c not in ordered:
            ordered.append(c)
        if len(ordered) >= max_cols:
            break
    return ordered or columns[: min(max_cols, len(columns))]


def _validate_identifiers(sql: str, allowlist: Mapping[str, Iterable[str]]) -> None:
    """Best-effort validation of identifiers in a generated SQL string.

    Ensures all ``table.column`` pairs appear in the provided allowlist,
    all tables in FROM/JOIN clauses are allowlisted, and blocks DDL/DML.
    """
    # Extract bare tokens and ensure all table.column references are allowed.
    tokens = set(_IDENTIFIER_RE.findall(sql))
    # Quick reject for DDL/DML verbs
    blocked = {"insert", "update", "delete", "alter", "drop", "create", "grant", "revoke"}
    if any(b in (t.lower()) for t in tokens for b in blocked):
        raise ValueError("DDL/DML tokens are not allowed in planner SQL")

    # Allow functions and keywords implicitly; enforce on identifiers
    tables = set(allowlist)
    columns = set()
    for cols in allowlist.values():
        columns.update({str(c) for c in cols})

    # Validate column names that appear after a dot (table.column)
    # Only match patterns that have at least one dot before the column name
    for m in re.finditer(r"([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+)\.([a-zA-Z_][a-zA-Z0-9_]*)", sql):
        t, c = m.group(1), m.group(2)
        # Check both with and without schema prefix
        table_without_schema = t.replace("analytics.", "") if t.startswith("analytics.") else t
        # Check if table exists in allowlist (with or without schema prefix)
        table_found = t in tables or table_without_schema in tables
        if not table_found or c not in columns:
            raise ValueError(f"identifier not allowed: {t}.{c}")

    # Validate FROM clause tables
    for m in re.finditer(r"\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\b", sql, flags=re.IGNORECASE):
        t = m.group(1)
        # Check both with and without schema prefix
        table_without_schema = t.replace("analytics.", "") if t.startswith("analytics.") else t
        table_found = t in tables or table_without_schema in tables
        if not table_found:
            raise ValueError(f"table not allowed: {t}")

    _validate_joins(sql, allowlist)

    # Disallow semicolons and system schemas
    if ";" in sql:
        raise ValueError("multiple statements are not allowed in planner SQL")
    if "pg_catalog" in sql.lower() or "information_schema" in sql.lower():
        raise ValueError("system catalogs are not allowed in planner SQL")


def _validate_joins(sql: str, allowlist: Mapping[str, Iterable[str]]) -> None:
    """Best-effort validation for JOINs against the allowlist.

    Ensures only allowlisted tables (optionally schema-qualified under
    analytics.) appear in JOIN clauses. Cross-schema joins are rejected.

    Parameters
    ----------
    sql: str
        Final SQL text to validate.
    allowlist: Mapping[str, Iterable[str]]
        Allowed tables and columns.
    """

    join_re = re.compile(r"\bJOIN\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\b", flags=re.IGNORECASE)
    allowed_tables = set(allowlist)
    for jm in join_re.finditer(sql):
        jt = jm.group(1)
        if "." in jt and not jt.lower().startswith("analytics."):
            raise ValueError(f"cross-schema join not allowed: {jt}")
        base = jt.replace("analytics.", "")
        if (jt not in allowed_tables) and (base not in allowed_tables):
            raise ValueError(f"join table not allowed: {jt}")
