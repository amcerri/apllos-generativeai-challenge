# Glossary

This document provides definitions for technical terms and concepts used throughout the Apllos Assistant system.

## Core Concepts

- **Agent**: A specialized component (analytics, knowledge, commerce, triage) responsible for a specific pipeline or domain
- **Allowlist**: Mapping of tables → columns that constrains the planner and informs routing decisions
- **Checkpointer**: Persistence backend for LangGraph threads/state management
- **Circuit Breaker**: Mechanism in executor to short-circuit repeated failures/timeouts
- **EXPLAIN**: Postgres plan introspection; optionally ANALYZE for runtime statistics
- **Heuristic**: Deterministic rule-based logic used when LLM is unavailable or to add guardrails
- **RAG**: Retrieval-Augmented Generation (retriever + ranker + answerer with citations)
- **RouterDecision**: Structured decision produced by the classifier
- **SQL Approval Gate**: Human-in-the-loop interrupt requesting approval before executing SQL

## System Components

- **Router**: LLM-based classifier that makes primary routing decisions
- **Supervisor**: Deterministic guardrails and fallback logic for routing
- **Planner**: Converts natural language to safe SQL queries
- **Executor**: Safely executes SQL queries with read-only transactions
- **Normalizer**: Converts raw data into human-readable PT-BR responses
- **Retriever**: Vector search for document retrieval using pgvector
- **Ranker**: Ranks retrieved documents by relevance
- **Answerer**: Generates answers with citations and cross-validation
- **Processor**: Extracts text from various document formats
- **Extractor**: Structured data extraction from documents
- **Summarizer**: Creates executive summaries with risk analysis

## Technical Terms

- **Chain-of-Thought**: LLM reasoning technique that shows step-by-step thinking
- **Self-Consistency**: LLM technique that validates responses for consistency
- **Confidence Calibration**: Process of adjusting confidence scores for accuracy
- **pgvector**: PostgreSQL extension for vector similarity search
- **IVFFLAT**: Vector index type for efficient similarity search
- **Embeddings**: Vector representations of text for semantic search
- **JSON Schema**: Structured format for LLM output validation
- **Circuit Breaker**: Pattern to prevent cascading failures
- **Graceful Degradation**: System continues operating with reduced functionality
- **Human-in-the-Loop**: Human approval required for certain operations
- **Read-Only Transaction**: Database transaction that prevents data modification
- **Statement Timeout**: Maximum time allowed for SQL query execution
- **Row Cap**: Maximum number of rows returned by a query
- **Deduplication**: Process of removing duplicate results
- **Cross-Validation**: Process of validating responses against multiple sources
- **Fallback**: Alternative behavior when primary method fails
- **Guardrails**: Safety mechanisms to prevent harmful operations
- **Observability**: Monitoring, logging, and tracing for system health
- **Structured Logging**: Logging with structured data for better analysis
- **Correlation ID**: Unique identifier for tracking requests across services
- **Metrics**: Quantitative measurements of system performance
- **Tracing**: Distributed tracing for request flow analysis
- **Prometheus**: Monitoring system for metrics collection
- **OpenTelemetry**: Observability framework for distributed systems

---

**← [Back to Documentation Index](../README.md)**
