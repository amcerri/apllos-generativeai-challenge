"""
Tracing utilities (optional OpenTelemetry integration).

Overview
    Minimal helpers to configure OpenTelemetry tracing (if installed) and to
    start spans safely. When OpenTelemetry is not available, all functions
    degrade to no-ops so importing this module is always safe.

Design
    - No hard dependency on OpenTelemetry; best‑effort lazy setup.
    - Small API: `configure()`, `get_tracer()`, `start_span()`, `current_trace_ids()`.
    - Log correlation: `start_span()` injects `trace_id` / `span_id` into the
      logging context so logs are automatically correlated.

Integration
    - Used by agent modules and graph nodes for distributed tracing.
    - Configure once at application startup via `configure()`.
    - Spans are automatically correlated with thread IDs and component names.

Usage
    >>> from app.infra.tracing import configure, start_span, current_trace_ids
    >>> configure(service_name="apllos-assistant", exporter="otlp-http", sample_ratio=0.1)
    >>> with start_span("router.classify", {"component": "routing"}):
    ...     pass
"""

from __future__ import annotations

import logging
from contextlib import AbstractContextManager, contextmanager, nullcontext
import uuid
from typing import Any, Mapping

# Attempt OpenTelemetry imports (optional dependency)
_OTEL_AVAILABLE = False
try:  # pragma: no cover - exercised only when opentelemetry is installed
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter as OTLPGrpcExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter as OTLPHTTPExporter,
    )
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
        SimpleSpanProcessor,
    )
    from opentelemetry.sdk.trace.sampling import (
        AlwaysOffSampler,
        ParentBased,
        TraceIdRatioBased,
    )
    from opentelemetry.trace import Span

    _OTEL_AVAILABLE = True
except Exception:  # pragma: no cover - keep optional
    trace = None
    TracerProvider = object
    Span = object

_log = logging.getLogger(__name__)
_service_name = "apllos-assistant"

__all__ = ["configure", "get_tracer", "start_span", "current_trace_ids"]


def _bool_env(value: str | None) -> bool:
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def configure(
    *,
    service_name: str = "apllos-assistant",
    exporter: str | None = "otlp-http",
    endpoint: str | None = None,
    headers: dict[str, str] | None = None,
    sample_ratio: float = 0.0,
) -> None:
    """Configure OpenTelemetry tracing if available.

    Parameters
    ----------
    service_name: Logical service name for trace resource attributes.
    exporter: One of {"otlp-http", "otlp-grpc", "console", None}. If None, no exporter.
    endpoint: OTLP endpoint; if None, uses exporter defaults / env vars.
    headers: Optional headers for OTLP HTTP exporter.
    sample_ratio: 0.0 disables (AlwaysOff); (0,1] uses TraceIdRatioBased via ParentBased.
    """

    global _service_name
    _service_name = service_name

    if not _OTEL_AVAILABLE:
        _log.info("opentelemetry not installed; tracing disabled")
        return

    # Sampler
    if sample_ratio <= 0.0:
        sampler = AlwaysOffSampler()
    else:
        sampler = ParentBased(TraceIdRatioBased(sample_ratio))

    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: service_name}),
        sampler=sampler,
    )

    # Exporters
    if exporter == "console":
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    elif exporter == "otlp-http":
        provider.add_span_processor(
            BatchSpanProcessor(OTLPHTTPExporter(endpoint=endpoint, headers=headers))
        )
    elif exporter == "otlp-grpc":
        provider.add_span_processor(BatchSpanProcessor(OTLPGrpcExporter(endpoint=endpoint)))
    elif exporter is None:
        pass
    else:
        _log.warning(
            "unknown tracing exporter '%s' — tracing configured without exporter", exporter
        )

    trace.set_tracer_provider(provider)


def get_tracer(component: str = "app") -> Any:
    """Return an OpenTelemetry tracer or a no‑op tracer when OTEL is absent."""

    if not _OTEL_AVAILABLE:
        return _NoopTracer()
    return trace.get_tracer(f"{_service_name}.{component}")


@contextmanager
def start_span(
    name: str, attributes: Mapping[str, Any] | None = None
) -> AbstractContextManager[Span | None]:
    """Context manager that starts a span and injects log correlation.

    Parameters
    ----------
    name : str
        Span name.
    attributes : Mapping[str, Any] | None
        Optional span attributes to set at start.

    Yields
    ------
    Span | None
        The active span when tracing is enabled; otherwise `None`.
    """

    # Late import to avoid cycles at import-time
    try:
        from app.infra.logging import bind_context, clear_context  # type: ignore
    except Exception:  # pragma: no cover - defensive fallback
        def bind_context(**_kw: Any) -> None:  # type: ignore
            return
        def clear_context(_keys: list[str] | None = None) -> None:  # type: ignore
            return

    if not _OTEL_AVAILABLE:
        # Generate ephemeral IDs to correlate logs even without OTEL
        trace_id = uuid.uuid4().hex
        span_id = uuid.uuid4().hex[:16]
        bind_context(trace_id=trace_id, span_id=span_id)
        try:
            yield None
        finally:
            clear_context(["trace_id", "span_id"])  # remove correlation keys
        return

    tracer = get_tracer("app")
    with tracer.start_as_current_span(name) as span:
        if attributes:
            for k, v in attributes.items():
                try:
                    span.set_attribute(k, v)
                except Exception:  # pragma: no cover - defensive
                    pass
        # Bind IDs into logging context for correlation
        tid, sid = current_trace_ids()
        if tid or sid:
            bind_context(trace_id=tid, span_id=sid)
        try:
            yield span
        finally:
            clear_context(["trace_id", "span_id"])  # remove correlation keys


def current_trace_ids() -> tuple[str | None, str | None]:
    """Return (trace_id_hex, span_id_hex) for the current context, or (None, None)."""

    if not _OTEL_AVAILABLE:
        # Best-effort read from logging context when OTEL is absent
        try:
            from app.infra.logging import _CTX  # type: ignore
            ctx = _CTX.get()
            return (ctx.get("trace_id"), ctx.get("span_id"))
        except Exception:  # pragma: no cover - optional
            return (None, None)
    try:
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if getattr(ctx, "is_valid", lambda: False)():
            trace_id = f"{ctx.trace_id:032x}"
            span_id = f"{ctx.span_id:016x}"
            return (trace_id, span_id)
    except Exception:  # pragma: no cover - defensive
        return (None, None)
    return (None, None)


class _NoopSpan:
    def __enter__(self):  # noqa: D401 - trivial
        return None

    def __exit__(self, exc_type, exc, tb):  # noqa: D401 - trivial
        return False


class _NoopTracer:
    def start_as_current_span(self, name: str):  # noqa: D401 - trivial
        return _NoopSpan()

    # Compatibility with usage as a context manager factory
    def __getattr__(self, item: str):  # noqa: D401 - trivial
        # Provide nullcontext for any unexpected attribute access used as context manager
        return nullcontext()
