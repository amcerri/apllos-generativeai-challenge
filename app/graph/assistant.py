"""
Assistant factory (entrypoint for LangGraph Server / Studio).

Overview
--------
Expose a single function `get_assistant()` that returns a compiled LangGraph
for our multi‑agent assistant (analytics, knowledge, commerce, triage). The
builder is delegated to `app.graph.build.build_graph`, and this module only
collects runtime switches (e.g., human‑in‑the‑loop gates) from optional
settings or environment variables.

Design
------
- Keep import‑time side effects minimal and optional.
- Provide resilient fallbacks for logging/tracing and for the graph builder.
- Make configuration discoverable via function argument or environment.

Integration
-----------
LangGraph Server should import: `app.graph.assistant:get_assistant`.

Usage
-----
>>> from app.graph.assistant import get_assistant
>>> graph = get_assistant({"require_sql_approval": False})
>>> bool(graph)
True
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional infra: logging & tracing with safe fallbacks
# ---------------------------------------------------------------------------
try:
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - simple fallback
        return _logging.getLogger(component)


start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# ---------------------------------------------------------------------------
# Graph builder (optional import)
# ---------------------------------------------------------------------------
try:
    from app.graph.build import build_graph as _build_graph
except Exception:  # pragma: no cover - optional
    _build_graph = None

# Global cache for compiled graphs
_GRAPH_CACHE: dict[tuple[bool], Any] = {}

# Global database configuration flag
_DB_CONFIGURED = False

# Global allowlist cache
_ALLOWLIST_CACHE: dict[str, Any] = {}

def clear_cache():
    """Clear the graph cache (useful for development)."""
    global _GRAPH_CACHE
    _GRAPH_CACHE.clear()

def _load_allowlist() -> dict[str, Any]:
    """Load allowlist from file."""
    global _ALLOWLIST_CACHE
    if _ALLOWLIST_CACHE:
        return _ALLOWLIST_CACHE
    
    # Hardcoded allowlist as fallback
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
    
    try:
        import json
        import os
        allowlist_path = os.path.join(os.path.dirname(__file__), "..", "routing", "allowlist.json")
        if os.path.exists(allowlist_path):
            with open(allowlist_path, 'r') as f:
                allowlist = json.load(f)
                log = get_logger("graph.assistant")
                log.info("Allowlist loaded from file", extra={"tables": list(allowlist.keys())})
        else:
            log = get_logger("graph.assistant")
            log.info("Using hardcoded allowlist", extra={"tables": list(allowlist.keys())})
    except Exception as e:
        log = get_logger("graph.assistant")
        log.warning("Failed to load allowlist from file, using hardcoded", extra={"error": str(e)})
    
    _ALLOWLIST_CACHE = allowlist
    return allowlist


__all__ = ["get_assistant"]

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------
_TRUE_SET: Final[set[str]] = {"1", "true", "yes", "on"}
_FALSE_SET: Final[set[str]] = {"0", "false", "no", "off"}


def _as_bool(v: Any, default: bool) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    s = str(v).strip().lower()
    if s in _TRUE_SET:
        return True
    if s in _FALSE_SET:
        return False
    return default


def _get_require_sql_approval(settings: Mapping[str, Any] | None) -> bool:
    # 1) Explicit function argument
    if settings and "require_sql_approval" in settings:
        return _as_bool(settings.get("require_sql_approval"), True)

    # 2) Nested settings keys (defensive)
    if settings:
        runtime = settings.get("runtime") if isinstance(settings, Mapping) else None
        if isinstance(runtime, Mapping) and "require_sql_approval" in runtime:
            return _as_bool(runtime.get("require_sql_approval"), True)

    # 3) Environment variables (first hit wins)
    for key in ("ASSISTANT_REQUIRE_SQL_APPROVAL", "REQUIRE_SQL_APPROVAL"):
        if key in os.environ:
            return _as_bool(os.environ.get(key), True)

    # 4) Default
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_assistant(settings: Mapping[str, Any] | None = None) -> Any:
    """Return a compiled graph (or stub) ready for LangGraph Server.

    Parameters
    ----------
    settings: Optional mapping with runtime switches.
    """
    log = get_logger("graph.assistant")

    require_sql_approval = _get_require_sql_approval(settings)
    
    # Configure database once globally
    global _DB_CONFIGURED
    if not _DB_CONFIGURED:
        try:
            import os
            
            dsn = os.environ.get("DATABASE_URL")
            if dsn:
                # Convert postgresql+psycopg:// to postgresql:// for SQLAlchemy
                if dsn.startswith("postgresql+psycopg://"):
                    dsn = dsn.replace("postgresql+psycopg://", "postgresql://")
                
                # Convert Docker internal hostname for external access
                if "@db:" in dsn:
                    dsn = dsn.replace("@db:", "@host.docker.internal:")
                
                from app.infra.db import ensure_db
                ensure_db()  # Initialize database connection
                log.info("Database configured successfully", extra={"dsn": dsn[:50] + "..." if len(dsn) > 50 else dsn})
                _DB_CONFIGURED = True
            else:
                log.warning("DATABASE_URL not set; database features disabled")
                _DB_CONFIGURED = True
        except Exception as e:
            log.warning("Failed to configure database", extra={"error": str(e)})
            _DB_CONFIGURED = True
    
    # Check cache first
    cache_key = (require_sql_approval,)
    if cache_key in _GRAPH_CACHE:
        log.info("Using cached graph", extra={"require_sql_approval": require_sql_approval})
        return _GRAPH_CACHE[cache_key]

    with start_span("assistant.get", {"require_sql_approval": require_sql_approval}):
        if _build_graph is not None:
            allowlist = _load_allowlist()
            graph = _build_graph(require_sql_approval=require_sql_approval, allowlist=allowlist)
            # Cache the compiled graph
            _GRAPH_CACHE[cache_key] = graph
        else:
            graph = {"engine": "stub", "nodes": [], "require_sql_approval": bool(require_sql_approval)}
        try:
            log.info(
                "Assistant graph ready",
                extra={
                    "require_sql_approval": require_sql_approval,
                    "has_nodes": bool(getattr(graph, "nodes", None)),
                },
            )
        except Exception:
            pass
        return graph


if __name__ == "__main__":  # pragma: no cover - convenience
    log = get_logger("graph.assistant")
    g = get_assistant({"require_sql_approval": False})
    kind = "compiled" if hasattr(g, "__class__") else "stub"
    try:
        log.info("assistant ready", extra={"kind": kind, "require_sql_approval": False})
    except Exception:
        pass
