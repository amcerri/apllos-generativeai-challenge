# Observability: Monitoring Guide

This document provides an overview of the observability system in the Apllos Assistant, including logging, metrics, tracing, and monitoring capabilities.

## Observability Overview

The Apllos Assistant implements a observability system with multiple layers of monitoring:

- **Logging**: Structured logging with context variables and correlation IDs
- **Metrics**: Prometheus-compatible metrics for performance monitoring
- **Tracing**: OpenTelemetry distributed tracing for request flow analysis
- **Health Checks**: Multiple health check endpoints for system status

## Logging System

### 1. Structured Logging
**Purpose**: Provide structured, searchable logs with context

**Features**:
- **JSON Format**: Machine-readable log format
- **Context Variables**: Request context and correlation IDs
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Correlation**: Track requests across services
- **Filtering**: Log filtering and search

**Implementation**:
```python
from app.infra.logging import get_logger

# Get logger with context
log = get_logger("agent.analytics").bind(
    thread_id="thr-123",
    user_id="user-456",
    request_id="req-789"
)

# Log with context
log.info("SQL generated", sql="SELECT * FROM orders", limit=200)
log.error("SQL execution failed", error="timeout", duration=120)
```

### 2. Log Context
**Purpose**: Maintain context across service boundaries

**Context Variables**:
- **thread_id**: Conversation thread identifier
- **user_id**: User identifier
- **request_id**: Request identifier
- **agent**: Current agent processing
- **node**: Current graph node
- **correlation_id**: Cross-service correlation

**Implementation**:
```python
from app.infra.logging import bind_context, clear_context

# Bind context
bind_context({
    "thread_id": "thr-123",
    "user_id": "user-456",
    "request_id": "req-789"
})

# Use context
log.info("Processing request")

# Clear context
clear_context()
```

### 3. Log Aggregation
**Purpose**: Centralize logs from multiple services

**Features**:
- **Centralized Collection**: Collect logs from all services
- **Search and Filter**: Log search capabilities
- **Retention**: Configurable log retention policies
- **Archival**: Long-term log archival
- **Analysis**: Log analysis and insights

## Metrics System

### 1. Prometheus Metrics
**Purpose**: Collect and expose system metrics

**Metric Types**:
- **Counters**: Cumulative metrics (requests, errors)
- **Histograms**: Distribution metrics (latency, duration)
- **Gauges**: Point-in-time metrics (memory, connections)
- **Summaries**: Quantile metrics (percentiles)

**Implementation**:
```python
from app.infra.metrics import get_metrics

# Get metrics instance
metrics = get_metrics()

# Record counter
metrics.counter("requests_total", {"agent": "analytics"}).inc()

# Record histogram
metrics.histogram("request_duration_seconds", {"agent": "analytics"}).observe(1.5)

# Record gauge
metrics.gauge("active_connections").set(42)
```

### 2. LLM Cost and Token Metrics
**Purpose**: Track LLM API costs and token usage for cost optimization

**LLM Metrics**:
- **`llm_cost_usd_total{model}`**: Cumulative LLM API cost in USD, labeled by model
- **`llm_tokens_total{model,type}`**: Token usage histogram, labeled by model and type (prompt/completion/total)

**Implementation**:
```python
from app.infra.metrics import inc_counter, observe_histogram

# Cost tracking (automatically done by LLMClient)
# Metrics are recorded automatically for all LLM interactions

# Manual token tracking (if needed)
observe_histogram("llm_tokens_total", value=1000, labels={"model": "gpt-4o-mini", "type": "prompt"})
observe_histogram("llm_tokens_total", value=500, labels={"model": "gpt-4o-mini", "type": "completion"})
```

**Cost Calculation**:
- Costs are calculated based on OpenAI's current pricing per million tokens
- Supports all OpenAI models (gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo, embeddings)
- Costs are tracked per model and aggregated in Prometheus

### 3. Custom Metrics
**Purpose**: Define custom metrics for business logic

**Custom Metrics**:
- **Agent Performance**: Agent-specific performance metrics
- **Routing Accuracy**: Routing decision accuracy
- **User Satisfaction**: User satisfaction scores
- **Business KPIs**: Business-specific metrics
- **Error Rates**: Error rates by component

**Implementation**:
```python
class CustomMetrics:
    def __init__(self):
        self.agent_requests = Counter("agent_requests_total", ["agent"])
        self.routing_accuracy = Histogram("routing_accuracy", ["agent"])
        self.user_satisfaction = Gauge("user_satisfaction_score")
        self.error_rate = Counter("error_rate_total", ["component"])
    
    def record_agent_request(self, agent: str):
        self.agent_requests.labels(agent=agent).inc()
    
    def record_routing_accuracy(self, agent: str, accuracy: float):
        self.routing_accuracy.labels(agent=agent).observe(accuracy)
    
    def record_user_satisfaction(self, score: float):
        self.user_satisfaction.set(score)
    
    def record_error(self, component: str):
        self.error_rate.labels(component=component).inc()
```

### 3. Metrics Endpoints
**Purpose**: Expose metrics for monitoring systems

**Endpoints**:
- **`/metrics`**: Prometheus metrics endpoint
- **`/health`**: Basic health check
- **`/ready`**: Readiness check
- **`/ok`**: Extended health check

**Implementation**:
```python
from fastapi import FastAPI
from app.infra.metrics import get_metrics

app = FastAPI()

# Mount metrics endpoint
metrics = get_metrics()
app.mount("/metrics", metrics.app)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/ok")
async def ok():
    return {
        "status": "ok",
        "db": "ok",
        "checkpointer": "ok"
    }
```

## Tracing System

### 1. OpenTelemetry Integration
**Purpose**: Distributed tracing for request flow analysis

**Features**:
- **Distributed Tracing**: Track requests across services
- **Span Correlation**: Correlate spans with logs and metrics
- **Performance Analysis**: Analyze request performance
- **Dependency Mapping**: Map service dependencies
- **Error Tracking**: Track errors across services

**Implementation**:
```python
from app.infra.tracing import start_span

# Start span
with start_span("agent.analytics.plan") as span:
    span.set_attribute("query", "SELECT * FROM orders")
    span.set_attribute("limit", 200)
    
    # Process request
    result = process_request()
    
    span.set_attribute("result_count", len(result))
```

### 2. Span Attributes
**Purpose**: Add context to traces

**Attribute Types**:
- **String**: Text attributes
- **Number**: Numeric attributes
- **Boolean**: Boolean attributes
- **Array**: Array attributes
- **Object**: Object attributes

**Implementation**:
```python
# Set span attributes
span.set_attribute("user_id", "user-123")
span.set_attribute("agent", "analytics")
span.set_attribute("confidence", 0.95)
span.set_attribute("tables", ["orders", "products"])
span.set_attribute("metadata", {"version": "1.0"})
```

### 3. Trace Correlation
**Purpose**: Correlate traces with logs and metrics

**Correlation Methods**:
- **Trace ID**: Unique trace identifier
- **Span ID**: Unique span identifier
- **Parent Span ID**: Parent span identifier
- **Correlation ID**: Cross-service correlation

**Implementation**:
```python
# Get trace context
trace_id = span.get_trace_id()
span_id = span.get_span_id()
parent_span_id = span.get_parent_span_id()

# Use in logs
log.info("Processing request", 
         trace_id=trace_id, 
         span_id=span_id,
         parent_span_id=parent_span_id)
```

## Health Monitoring

### 1. Health Checks
**Purpose**: Monitor system health and availability

**Check Types**:
- **Liveness**: Basic system liveness
- **Readiness**: System readiness for requests
- **Extended Health**: Health check
- **Dependency Health**: External dependency health

**Implementation**:
```python
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/ok")
async def ok():
    return {
        "status": "ok",
        "db": check_database(),
        "checkpointer": check_checkpointer(),
        "llm": check_llm_client()
    }
```

### 2. Dependency Monitoring
**Purpose**: Monitor external dependencies

**Dependencies**:
- **Database**: PostgreSQL connection and health
- **LLM Client**: OpenAI API availability
- **Vector Store**: pgvector availability
- **Checkpointer**: LangGraph checkpointer health

**Implementation**:
```python
def check_database():
    try:
        with open_connection() as conn:
            conn.execute("SELECT 1")
        return "ok"
    except Exception as e:
        return f"down: {str(e)}"

def check_llm_client():
    try:
        client = get_llm_client()
        client.health_check()
        return "ok"
    except Exception as e:
        return f"down: {str(e)}"
```

---

**← [Back to Documentation Index](../README.md)**