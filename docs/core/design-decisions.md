# Architectural Decisions (ADRs)

This document provides a curated list of significant design decisions and their rationale, explaining the architectural choices that shape the Apllos Assistant system.

## ADR-001: Optional Dependencies and Graceful Degradation

**Decision**: All heavy dependencies (FastAPI, LangGraph, OpenAI, SQLAlchemy, Prometheus, OpenTelemetry) are optional at import time. Modules provide stubs/no-ops when unavailable.

**Rationale**: 
- Keep tests deterministic and fast
- Enable partial functionality without full stack
- Improve developer experience (DX)
- Allow deployment in constrained environments
- Facilitate testing without external dependencies

**Consequences**: 
- Feature flags and fallbacks must be maintained
- Some behavior differs between development and fully provisioned environments
- Requires careful handling of optional imports
- Testing must cover both full and minimal configurations

**Implementation**: Uses try/except blocks for optional imports and provides no-op implementations when dependencies are unavailable.

## ADR-002: Context-First Routing with Single-Pass Fallback

- Decision: Use an LLM classifier with deterministic supervisor guardrails and allow at most one fallback.
- Rationale: Reduce oscillations and ensure predictable behavior under uncertainty; emphasize structural cues (allowlist, SQL shape).
- Consequences: Some ambiguous requests may route conservatively to triage or single fallback.

## ADR-003: Analytics Safety (Planner/Executor)

- Decision: Enforce allowlist, block cross-schema joins, require LIMIT on non-aggregates; executor read-only, statement timeouts, client row caps, and EXPLAIN-only dry-run on rejection.
- Rationale: Prevent harmful or expensive queries; maintain user trust with approvals.
- Consequences: Some complex queries require adjustments; human approval adds latency when enabled.

## ADR-004: RAG with Deterministic Fallbacks

- Decision: Retriever uses embeddings with deterministic fallback; ranker is heuristic with optional LLM reranker; answerer can fallback to extractive summarization.
- Rationale: Ensure the assistant remains useful when LLMs are degraded.
- Consequences: Answer quality may vary; citations always included to maintain traceability.

## ADR-005: Commerce Documents via Hybrid Extraction

- Decision: LLM structured output first, with heuristic reconciliation of totals; processor supports OCR and multi-format.
- Rationale: Balance accuracy and robustness across diverse document layouts.
- Consequences: LLM costs present; OCR introduces latency; provide warnings and risks for operator visibility.

## ADR-006: Centralized LLM Client

- Decision: Single wrapper handles timeouts, retries, JSON extraction for all components.
- Rationale: Consistency, observability, and controlled failure behavior.
- Consequences: Client abstraction must track provider API changes.

## ADR-007: LLM-First Approach with State-of-the-Art Prompt Engineering

- Decision: Prioritize LLM decisions over heuristic rules across all agents, implementing Chain-of-Thought reasoning, self-consistency checks, and confidence calibration.
- Rationale: Improve decision quality, reduce hardcoded logic, and provide more intelligent, human-like responses.
- Consequences: Increased LLM usage and latency, but significantly better user experience and analytical insights.

## ADR-008: Intelligent Data Balancing in Analytics

- Decision: Implement LLM-first intelligent data balancing with configurable thresholds to decide between complete data display vs. analytical insights.
- Rationale: Provide optimal user experience by showing complete data for small datasets and intelligent analysis for large datasets.
- Consequences: More sophisticated decision-making, configurable thresholds (default 100 records), and human-like responses instead of raw SQL outputs.

## ADR-009: Enhanced Routing with Critical Override Rules

- Decision: Implement enhanced validation with critical override rules for conceptual questions, document processing, data queries, and greetings in the routing classifier.
- Rationale: Ensure correct routing of edge cases and improve overall system reliability.
- Consequences: More complex routing logic but significantly better classification accuracy for edge cases.

---

**← [Back to Documentation Index](../README.md)**
