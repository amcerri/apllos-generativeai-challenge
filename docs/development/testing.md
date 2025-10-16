# Testing Strategy and Guardrails

This document provides comprehensive details about the testing strategy, safety guarantees, and validation mechanisms that ensure the Apllos Assistant operates reliably and safely.

## Testing Overview

The testing strategy is designed to ensure system reliability, safety, and performance across all components:

- **Unit Tests**: Validate individual components and safety mechanisms
- **Integration Tests**: Test component interactions and data flows
- **End-to-End Tests**: Validate complete user workflows
- **Batch Tests**: Performance and regression testing with real data
- **Safety Tests**: Validate security and guardrail mechanisms

## Test Structure

### Unit Tests (`tests/unit/*`)

**Purpose**: Validate individual components, algorithms, and safety mechanisms

**Coverage**:
- **Analytics Planner**: Heuristics, joins, properties, allowlist validation
- **Analytics Executor**: Guards, circuit breaker, SQL safety
- **Knowledge Retrieval**: Vector search, ranking, deduplication
- **Commerce Extraction**: Heuristics, parsing, validation
- **Router Contract**: Decision structure, validation, signals
- **Triage Handler**: Fallback logic, guidance generation

**Key Safety Assertions**:
- Planner enforces allowlist identifiers and blocks cross-schema joins
- Executor only allows SELECT/WITH statements with read-only transactions
- Knowledge retrieval uses min_score thresholds and deduplication
- Commerce extraction validates totals and flags inconsistencies
- Router decisions are properly structured and validated

### End-to-End Tests (`tests/e2e/*`)

**Purpose**: Validate complete user workflows and system integration

**Test Categories**:
- **Human Gates**: SQL approval workflow and interrupt handling
- **Routing Paths**: Complete routing from query to response
- **Agent Workflows**: Full agent pipeline execution
- **Error Handling**: Graceful degradation and fallback scenarios

**Key Validations**:
- Complete query-to-response workflows
- Human approval gates for SQL execution
- Routing accuracy across different query types
- Error recovery and fallback mechanisms

### Batch Tests (`tests/batch/*.yaml`)

**Purpose**: Performance testing and regression validation with real data

**Test Scenarios**:
- **Analytics**: Complex SQL queries and data analysis
- **Knowledge**: RAG retrieval and answer generation
- **Commerce**: Document processing and extraction
- **Routing**: Classification accuracy and performance

**Performance Metrics**:
- Response time benchmarks
- Memory usage patterns
- LLM token consumption
- Database query performance

## Key Safety Assertions

- Planner:
  - Enforces allowlist identifiers, blocks cross-schema joins, requires LIMIT on non-aggregate queries, fixes schema prefixes and alias issues.
- Executor:
  - Only SELECT/WITH, forbids DDL/DML and unknown functions; statement timeout, client row caps; EXPLAIN-only dry run on rejected approvals; circuit breaker opens on repeated failures.
- Knowledge:
  - Retrieval with min_score threshold; dedupe per `doc_id`; ranker deterministic; answerer returns citations.
- Commerce:
  - Heuristic extraction parses items/totals; reconciles components to detect inconsistencies; flags risks.
- Routing:
  - RouterDecision contract is strict; supervisor applies single-pass fallbacks; confidence bounds enforced.

## Human-in-the-Loop

- [app/graph/interrupts.py](../app/graph/interrupts.py) provides `make_sql_gate` used by analytics executor when `require_sql_approval=true`.
- E2E test checks shape/serializability of gates and the graph builder toggle.

## CI Considerations

- Tests avoid hard dependencies where possible; modules degrade to stubs; network calls are avoided in unit tests.

---

**← [Back to Documentation Index](../README.md)**
