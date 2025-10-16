# FAQ: Frequently Asked Questions

This document provides answers to frequently asked questions about the Apllos Assistant system.

## General Questions

### Q: What is the Apllos Assistant?
**A**: The Apllos Assistant is a multi-agent system built with LangGraph that provides assistance for e-commerce analytics, knowledge retrieval (RAG), and commerce document processing. It uses LLM-first approaches with fallbacks.

### Q: What are the main features of the system?
**A**: The system offers:
- **Multi-Agent Architecture**: Four specialized agents (Analytics, Knowledge, Commerce, Triage)
- **LLM-First Design**: Prompt engineering with Chain-of-Thought reasoning
- **Fallbacks**: Deterministic heuristics when LLMs are unavailable
- **Safety**: SQL allowlists and read-only execution
- **Observability**: Logging, metrics, and tracing
- **Portuguese Language**: Native support for Brazilian Portuguese responses

### Q: How does the routing system work?
**A**: The routing system uses a two-stage approach:
1. **Router (LLM Classifier)**: Makes routing decisions using LLM
2. **Supervisor**: Applies deterministic guardrails and fallback logic
3. **Probes**: Evidence-gathering mechanisms for context-aware routing

### Q: What agents are available?
**A**: The system includes four specialized agents:
- **Analytics Agent**: Converts natural language to safe SQL and provides data analysis
- **Knowledge Agent (RAG)**: Retrieves and synthesizes information from document knowledge base
- **Commerce Agent**: Processes commercial documents and extracts structured data
- **Triage Agent**: Handles ambiguous queries and provides guidance

## Technical Questions

### Q: What technologies are used?
**A**: The system uses:
- **LangGraph**: Multi-agent orchestration
- **PostgreSQL**: Database with pgvector extension
- **OpenAI API**: LLM processing and embeddings
- **FastAPI**: REST API server
- **Docker**: Containerization

### Q: How do I set up the system?
**A**: Quick setup:
```bash
# Clone and setup
git clone https://github.com/amcerri/apllos-generativeai-challenge.git
cd apllos-generativeai-challenge

# Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Full bootstrap
make bootstrap-complete
```

### Q: What data is used?
**A**: The system uses:
- **Analytics Data**: Olist e-commerce dataset
- **Knowledge Data**: Document chunks with vector embeddings
- **Commerce Data**: Sample commercial documents
- **Configuration**: YAML-based configuration files

### Q: How secure is the system?
**A**: The system implements security measures:
- **SQL Safety**: Allowlist-based SQL validation
- **Read-only**: Analytics queries are read-only
- **Timeouts**: Query timeouts and resource limits
- **Validation**: Input validation and sanitization

## Usage Questions

### Q: How do I query the system?
**A**: You can query the system using:
- **CLI**: `make query QUERY="your question"`
- **LangGraph Studio**: Web interface at `http://localhost:2024`
- **API**: REST API endpoints

### Q: What types of queries are supported?
**A**: The system supports:
- **Analytics**: "Quantos pedidos existem no total?"
- **Knowledge**: "Quais são as melhores práticas de precificação?"
- **Commerce**: "Analise este documento" (with attachment)
- **General**: Any natural language query

### Q: How do I add documents to the knowledge base?
**A**: Add documents to `data/docs/` folder and run:
```bash
make ingest-vectors
```

### Q: How do I add new data to analytics?
**A**: Add CSV files to `data/raw/analytics/` and run:
```bash
make ingest-analytics
make gen-allowlist
```

## Troubleshooting Questions

### Q: The database is not responding
**A**: Check database status:
```bash
make db-status
make db-stop && make db-start
```

### Q: OpenAI API calls are failing
**A**: Verify your API key:
```bash
echo $OPENAI_API_KEY
```

### Q: The system is slow
**A**: Check:
- Database performance: `make db-psql -c "ANALYZE doc_chunks;"`
- Application logs: `make logs`
- Health status: `curl http://localhost:2024/ok`

### Q: How do I check system health?
**A**: Use health check endpoints:
```bash
curl http://localhost:2024/ok
curl http://localhost:2024/health
curl http://localhost:2024/ready
```

## Development Questions

### Q: How do I contribute to the project?
**A**: See the [Development Guide](../development/configuration.md) for detailed instructions.

### Q: How do I run tests?
**A**: Run tests using:
```bash
make test
make test-unit
make test-e2e
```

### Q: How do I add a new agent?
**A**: See the [Development Guide](../development/configuration.md) for instructions on adding new agents.

### Q: How do I customize the system?
**A**: The system is highly configurable through:
- Environment variables
- YAML configuration files
- Custom prompts
- Model configurations

This FAQ provides answers to common questions about the Apllos Assistant system.
---

**← [Back to Documentation Index](../README.md)**
