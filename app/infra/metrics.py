"""
Analytics agent package initializer

Overview
    Side‑effect‑free initializer for the **analytics** agent. This package will
    contain three stages executed in order: **planner** → **executor** → **normalize**.
    The agent answers tabular questions over Olist data through **safe SQL** using
    an allowlist; the final user response is business‑friendly in pt‑BR.

Design
    - Keep this module lightweight (no I/O, no dynamic imports).
    - Do **not** import submodules here to avoid early side effects/cycles.
    - Provide discovery helpers that return **paths** to stage modules.

Integration
    - Other parts of the app can inspect available stages via `stages()` and
      resolve `stage_path(name)` without importing the stage implementations yet.

Usage
    >>> from app.agents.analytics import stages, has_stage, stage_path
    >>> stages()
    ('planner', 'executor', 'normalize')
    >>> has_stage('planner')
    True
    >>> stage_path('normalize').name
    'normalize.py'
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

_log = logging.getLogger(__name__)

__all__ = [
    "configure_metrics",
    "inc_counter",
    "observe_histogram",
    "set_gauge",
    "metrics_available",
]


# Optional prometheus_client import (no hard dependency)
_PROM: Any | None = None
try:  # pragma: no cover - optional dependency
    from prometheus_client import Counter as _Counter  # type: ignore
    from prometheus_client import Histogram as _Histogram  # type: ignore
    from prometheus_client import Gauge as _Gauge  # type: ignore
    from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest  # type: ignore

    _PROM = {
        "Counter": _Counter,
        "Histogram": _Histogram,
        "Gauge": _Gauge,
        "CollectorRegistry": CollectorRegistry,
        "CONTENT_TYPE_LATEST": CONTENT_TYPE_LATEST,
        "generate_latest": generate_latest,
    }
except Exception:
    _PROM = None


_REGISTRY: Any | None = None
_COUNTERS: dict[str, Any] = {}
_HISTOGRAMS: dict[str, Any] = {}
_GAUGES: dict[str, Any] = {}


def metrics_available() -> bool:
    """Return True when prometheus client is available.

    Returns
    -------
    bool
        Whether prometheus_client could be imported.
    """

    return _PROM is not None


def configure_metrics(namespace: str = "apllos", subsystem: str | None = None) -> None:
    """Configure a local metrics registry and a few default series.

    Parameters
    ----------
    namespace: str
        Prometheus metric namespace/prefix.
    subsystem: str | None
        Optional subsystem to include in metric names.
    """

    global _REGISTRY
    if _PROM is None:
        _log.info("prometheus_client not available; metrics disabled")
        return

    if _REGISTRY is None:
        _REGISTRY = _PROM["CollectorRegistry"]()

    def _name(base: str) -> str:
        return "_".join([p for p in (namespace, subsystem, base) if p])

    # Default counters/histograms used across the app (created lazily on first use too)
    _COUNTERS.setdefault(
        "requests_total",
        _PROM["Counter"](
            _name("requests_total"),
            "Total assistant requests by agent/node",
            ["agent", "node"],
            registry=_REGISTRY,
        ),
    )
    _COUNTERS.setdefault(
        "routing_fallbacks_total",
        _PROM["Counter"](
            _name("routing_fallbacks_total"),
            "Routing fallbacks applied by supervisor",
            ["from_agent", "to_agent"],
            registry=_REGISTRY,
        ),
    )
    _COUNTERS.setdefault(
        "llm_failures_total",
        _PROM["Counter"](
            _name("llm_failures_total"),
            "LLM request failures by component",
            ["component"],
            registry=_REGISTRY,
        ),
    )
    _HISTOGRAMS.setdefault(
        "node_latency_ms",
        _PROM["Histogram"](
            _name("node_latency_ms"),
            "Node execution latency in milliseconds",
            ["node"],
            buckets=(50, 100, 250, 500, 1000, 2500, 5000),
            registry=_REGISTRY,
        ),
    )
    _COUNTERS.setdefault(
        "llm_cost_usd_total",
        _PROM["Counter"](
            _name("llm_cost_usd_total"),
            "Total LLM API cost in USD",
            ["model"],
            registry=_REGISTRY,
        ),
    )
    _HISTOGRAMS.setdefault(
        "llm_tokens_total",
        _PROM["Histogram"](
            _name("llm_tokens_total"),
            "Total LLM tokens used",
            ["model", "type"],
            buckets=(100, 500, 1000, 2500, 5000, 10000, 25000, 50000),
            registry=_REGISTRY,
        ),
    )


def inc_counter(name: str, labels: Mapping[str, str] | None = None, amount: float = 1.0) -> None:
    """Increment a named counter if metrics are enabled.

    Parameters
    ----------
    name: str
        Logical counter name (e.g., "requests_total").
    labels: Mapping[str, str] | None
        Label set to use when incrementing the series.
    amount: float
        Increment amount (default 1.0).
    """

    if _PROM is None:
        return
    if name not in _COUNTERS:
        return
    try:
        s = _COUNTERS[name]
        s.labels(**dict(labels or {})).inc(amount)
    except Exception:
        # Never break request flow due to metrics
        pass


def observe_histogram(name: str, value_ms: float, labels: Mapping[str, str] | None = None) -> None:
    """Observe a value in a histogram when available.

    Parameters
    ----------
    name: str
        Logical histogram name (e.g., "node_latency_ms").
    value_ms: float
        Latency/value in milliseconds.
    labels: Mapping[str, str] | None
        Label set for the observation.
    """

    if _PROM is None:
        return
    if name not in _HISTOGRAMS:
        return
    try:
        _HISTOGRAMS[name].labels(**dict(labels or {})).observe(float(value_ms))
    except Exception:
        pass


def set_gauge(name: str, value: float, labels: Mapping[str, str] | None = None) -> None:
    """Set a gauge value if the series exists.

    Parameters
    ----------
    name: str
        Logical gauge name.
    value: float
        Gauge value to set.
    labels: Mapping[str, str] | None
        Label set for the observation.
    """

    if _PROM is None:
        return
    g = _GAUGES.get(name)
    if g is None:
        return
    try:
        g.labels(**dict(labels or {})).set(float(value))
    except Exception:
        pass


# Utilities for exposing metrics in ASGI servers --------------------------------
def asgi_metrics_app():  # pragma: no cover - integration helper only
    """Return a minimal ASGI app that serves Prometheus metrics.

    Returns
    -------
    Any
        ASGI app callable or None when prometheus is unavailable.
    """

    if _PROM is None or _REGISTRY is None:
        return None

    async def app(scope, receive, send):  # type: ignore[no-untyped-def]
        if scope["type"] != "http":
            return
        content = _PROM["generate_latest"](_REGISTRY)
        headers = [(b"content-type", _PROM["CONTENT_TYPE_LATEST"].encode("utf-8"))]
        await send({"type": "http.response.start", "status": 200, "headers": headers})
        await send({"type": "http.response.body", "body": content})

    return app


