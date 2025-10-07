# Apllos Assistant Documentation

This documentation set provides an in-depth, implementation-level reference for the multi-agent assistant, covering architecture, graph orchestration, agents, routing, infrastructure, configuration, contracts, prompts/data/scripts, testing, operations, and design decisions. It targets engineers who will operate, extend, or audit the system.

- Audience: senior engineers, SREs, data/ML engineers
- Scope: end-to-end technical documentation, including rationale and guardrails

## Index

- Architecture and Graph Orchestration: see `architecture.md`
- API Server and Endpoints: see `api.md`
- Agents
  - Analytics: `agents/analytics.md`
  - Knowledge (RAG): `agents/knowledge.md`
  - Commerce: `agents/commerce.md`
  - Triage: `agents/triage.md`
- Routing (Classifier, Supervisor, Allowlist): `routing.md`
- Infrastructure (LLM client, DB, Logging, Metrics, Tracing, Checkpointer): `infra.md`
- Configuration and Models Settings: `configuration.md`
- Contracts and Utilities: `contracts_utils.md`
- Prompts, Data, and Scripts: `prompts_data_scripts.md`
- Testing Strategy and Guardrails: `testing.md`
- Operations and Troubleshooting: `operations.md`
- Glossary: `glossary.md`
- Architectural Decisions (ADRs): `design-decisions.md`

## How to Read

- Start with `architecture.md` for a mental model.
- Use agent-specific docs when working on a pipeline.
- Refer to `testing.md` to understand non-functional guarantees and safety.
- Use `operations.md` for runbooks and common issues.

## Conventions

- Code references use repository-relative paths.
- Configuration paths refer to `app/config/*.yaml` and `Settings` models.
- Metrics names follow the Prometheus style documented in `infra.md`.
