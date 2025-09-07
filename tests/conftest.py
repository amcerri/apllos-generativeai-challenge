"""
Pytest configuration and shared fixtures.

Overview
--------
Shared test utilities for the assistant POC. Fixtures here avoid network/
external side effects, provide minimal configuration, and expose commonly used
objects such as the assistant instance and an analytics allowlist snapshot.

Design
------
- Pure‑Python, dependency‑light; optional imports are guarded.
- Defaults to a safe, isolated environment (APP_ENV=test, no tracing).
- Assistant fixture builds the graph via `app.graph.assistant.get_assistant`,
  which already degrades gracefully if optional deps are missing.

Integration
-----------
The tests in this POC do not require a running Postgres or LangGraph Studio.
Where DB or embeddings are needed, unit tests should mock per‑test. This file
only sets environment defaults and provides deterministic sample data.

Usage
-----
Import fixtures in tests by name (e.g., `assistant`, `allowlist`).
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, cast

import pytest

# ---------------------------------------------------------------------------
# Environment isolation (applies to every test)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _isolation_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Set safe defaults and isolate noisy integrations for all tests."""
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    # Avoid real network calls by default; tests can override as needed
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    # Provide a harmless default; unit tests that require DB should override
    monkeypatch.setenv(
        "DATABASE_URL",
        os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/postgres"),
    )
    # Disable tracing by default
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
    monkeypatch.delenv("OTEL_SERVICE_NAME", raising=False)
    # LangGraph/Studio opt-outs (if referenced by runtime)
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")
    monkeypatch.setenv("LANGGRAPH_SERVER_ENABLED", "false")


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def to_dict(obj: Any) -> Any:
    """Best‑effort conversion of dataclasses to plain dict for assertions."""
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list | tuple):
        return [to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj


# ---------------------------------------------------------------------------
# Settings and assistant fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def settings() -> Mapping[str, Any]:
    """Load settings via app.config if available, otherwise minimal dict."""
    try:
        import importlib

        cfg = importlib.import_module("app.config")
        getter = getattr(cfg, "get_settings", None)
        if callable(getter):
            return cast(Mapping[str, Any], to_dict(getter()))
    except Exception:
        pass
    return {
        "env": "test",
        "confidence_min": 0.3,
        "retrieval_min_score": 0.2,
        "require_sql_approval": True,
    }


@pytest.fixture(scope="session")
def assistant(settings: Mapping[str, Any]) -> Any:
    """Build an assistant instance using the project factory.

    The factory in `app.graph.assistant` provides a stub when optional
    dependencies are not installed, which is sufficient for unit tests.
    """
    try:
        from app.graph.assistant import get_assistant

        return get_assistant(settings)
    except Exception:  # pragma: no cover - defensive
        # Provide a tiny stub compatible with the tests that only check wiring
        class _Stub:
            def __init__(self, cfg: Mapping[str, Any]):
                self.config = dict(cfg)

            def __repr__(self) -> str:  # pragma: no cover - trivial
                return f"AssistantStub(env={self.config.get('env','test')})"

        return _Stub(settings)


# ---------------------------------------------------------------------------
# Deterministic sample allowlist for analytics planner tests
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def allowlist() -> dict[str, list[str]]:
    """A compact snapshot aligned with `data/samples/schema.sql`."""
    return {
        "customers": [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ],
        "geolocation": [
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_city",
            "geolocation_state",
        ],
        "orders": [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
        "products": [
            "product_id",
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
        "sellers": [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
        ],
        "order_items": [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
        ],
        "order_payments": [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ],
        "order_reviews": [
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_creation_date",
            "review_answer_timestamp",
        ],
        "product_category_translation": [
            "product_category_name",
            "product_category_name_english",
        ],
    }


# ---------------------------------------------------------------------------
# Optional: FastAPI test client (only if FastAPI is installed)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def api_client(settings: Mapping[str, Any]) -> Any:
    """Provide a TestClient if FastAPI is available; otherwise return None."""
    try:
        from fastapi.testclient import TestClient

        from app.api.server import get_app

        app = get_app(settings)
        return TestClient(app)
    except Exception:
        return None
