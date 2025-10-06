# Apllos Generative AI Challenge

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org) [![LangGraph](https://img.shields.io/badge/LangGraph-0.4+-green.svg)](https://langchain-ai.github.io/langgraph/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org) [![Docker](https://img.shields.io/badge/Docker-20+-blue.svg)](https://docker.com) [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com)

> **Multi-Agent Intelligent System for E-commerce Data Analysis**  
> Advanced generative AI platform that combines Knowledge Retrieval, Analytics, and Commerce Processing in a unified architecture powered by LangGraph.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation & Configuration](#installation--configuration)
- [Usage Guide](#usage-guide)
- [Agents](#agents)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Monitoring & Observability](#monitoring--observability)
- [Contributing](#contributing)
- [Support](#support)

---

## Overview

The **Apllos Generative AI Challenge** is a sophisticated multi-agent intelligent system designed for comprehensive e-commerce data analysis. Built on LangGraph, it combines three specialized agents to provide deep insights into commercial data through natural language interactions.

### Key Features

- **Multi-Agent Intelligence**: Coordinated system with specialized agents for different data types
- **Advanced Analytics**: Complex SQL analysis with security validation and business insights
- **Knowledge Retrieval**: RAG system for semantic document search and contextual responses
- **Commerce Processing**: Intelligent processing of commercial documents (PDF, DOCX, TXT)
- **Security First**: Rigorous SQL query validation, allowlist enforcement, and access control
- **Observability**: Structured logging, distributed tracing, and comprehensive monitoring
- **Containerized**: Simplified deployment with Docker and Docker Compose
- **Multi-Interface**: CLI and REST API for different use cases

### Use Cases

- **Performance Analysis**: Sales metrics, customer churn, growth analysis, KPI tracking
- **Product Insights**: Top products, category analysis, contribution margins, inventory optimization
- **Geographic Analysis**: Performance by state/region, market penetration, regional trends
- **Document Processing**: Order analysis, invoice processing, contract summarization
- **Business Consulting**: Strategic questions, best practices, market insights
- **Knowledge Discovery**: Semantic search across documents, contextual information retrieval

---

## Architecture

### System Architecture

```mermaid
graph TB
    subgraph "Interface Layer"
        CLI[Command Line<br/>Interface]
        API[REST API<br/>FastAPI]
        STUDIO[LangGraph Studio<br/>Debug Interface]
    end
    
    subgraph "Orchestration Layer"
        LG[LangGraph<br/>Orchestrator]
        RT[Router &<br/>Triage System]
        SP[Supervisor<br/>Rules Engine]
    end
    
    subgraph "Agent Layer"
        KA[Knowledge Agent<br/>RAG System]
        AA[Analytics Agent<br/>SQL Engine]
        CA[Commerce Agent<br/>Document Processor]
        TR[Triage Handler<br/>Error Management]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Analytics Data)]
        VEC[(pgvector<br/>Document Embeddings)]
        DOCS[Document Store<br/>PDF/DOCX/TXT]
    end
    
    subgraph "External Services"
        OAI[OpenAI API<br/>GPT-4o-mini]
        EMB[Embeddings<br/>text-embedding-3-small]
    end
    
    CLI --> API
    STUDIO --> LG
    API --> RT
    RT --> SP
    SP --> KA
    SP --> AA
    SP --> CA
    SP --> TR
    KA --> VEC
    AA --> PG
    CA --> DOCS
    KA --> OAI
    AA --> OAI
    CA --> OAI
    VEC --> EMB
```

### Core Components

#### **1. LangGraph Orchestrator**

- **Function**: Request coordination, routing, and state management
- **Technology**: LangGraph 0.4+ with native checkpointing
- **Features**: Persistent state, human-in-the-loop gates, conditional routing

#### **2. Router & Triage System**

- **Function**: Intelligent request classification and routing
- **Technology**: OpenAI GPT-4o-mini with structured outputs
- **Features**: Context-first routing, confidence scoring, fallback mechanisms

#### **3. Knowledge Agent (RAG)**

- **Function**: Retrieval Augmented Generation for document queries
- **Technology**: pgvector + OpenAI Embeddings + GPT-4o-mini
- **Features**: Semantic search, intelligent ranking, mandatory citations

#### **4. Analytics Agent**

- **Function**: Complex SQL analysis with security and business insights
- **Technology**: PostgreSQL + SQLAlchemy + GPT-4o-mini
- **Features**: Safe SQL generation, allowlist validation, Portuguese normalization

#### **5. Commerce Agent**

- **Function**: Commercial document processing and structured extraction
- **Technology**: python-docx + OCR + GPT-4o-mini + JSON Schema
- **Features**: Multi-format support, structured extraction, intelligent summaries

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/amcerri/apllos-generativeai-challenge.git
cd apllos-generativeai-challenge

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your OpenAI API key

# 3. Start the complete system
make bootstrap-complete

# 4. Access LangGraph Studio
make studio-up
# Open [LangGraph Studio](https://smith.langchain.com/studio/?baseUrl=http://localhost:2024)
```

### Option 2: Local Development

```bash
# 1. Install dependencies
pip install -e .

# 2. Configure database
make db-start
make db-wait
make db-init
make db-seed

# 3. Ingest data
make ingest-analytics
make ingest-vectors

# 4. Start services
make studio-up
```

### Quick Test

```bash
# Test analytics query
make query QUERY="How many orders exist in total?"

# Test commerce query with document
make query QUERY="Analyze this order" ATTACHMENT="data/samples/orders/Simple Order.docx"

# Test knowledge query
make query QUERY="What are the best practices for e-commerce pricing?"
```

---

## Installation & Configuration

### Prerequisites

- **Python**: 3.11+
- **Docker**: 20.0+
- **Docker Compose**: 2.0+
- **OpenAI API Key**: Required for LLM functionality
- **PostgreSQL**: 15+ (or use Docker)

### Environment Configuration

#### 1. **Environment Variables**

Create a `.env` file based on `.env.example`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Database Configuration
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app

# Application Configuration
LOG_LEVEL=INFO
DEBUG=false
REQUIRE_SQL_APPROVAL=false

# LangGraph Configuration
LANGGRAPH_SERVER_PORT=2024
LANGGRAPH_STUDIO_PORT=2025

```

#### 2. **Database Setup**

```bash
# Start PostgreSQL with pgvector
make db-start

# Wait for initialization
make db-wait

# Create schema and extensions
make db-init

# Load sample data
make db-seed
```

#### 3. **Data Ingestion**

```bash
# Ingest analytics data (Olist CSVs)
make ingest-analytics

# Ingest documents for RAG (PDFs, TXT, MD)
make ingest-vectors

# Generate allowlist from schema
make gen-allowlist

# Ingest everything at once
make ingest-all
```

### Docker Configuration

The system uses Docker Compose for orchestration:

```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
      - "2024:2024"
      - "2025:2025"
    environment:
      - DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
    depends_on:
      - db
```
---

## Usage Guide

### LangGraph Studio (Debug Interface)

1. **Access Studio**: [LangGraph Studio](https://smith.langchain.com/studio/?baseUrl=http://localhost:2024)
2. **Configure Thread**: Use a thread ID to maintain context across queries
3. **Ask Questions**: Type queries in natural language
4. **Attach Documents**: For commercial document analysis
5. **View Execution**: Monitor agent execution and decision flow

### Command Line Interface

#### **Basic Queries**

```bash
# Simple analytics query
make query QUERY="What is the total sales revenue?"

# Query with thread context
make query QUERY="What was the growth in the last quarter?" THREAD_ID="thread_123"

# Query with document attachment
make query QUERY="Analyze this order" ATTACHMENT="data/samples/orders/Order.docx"
```

#### **Batch Processing**

```bash
# Process multiple queries from 
make batch-query INPUT="tests/batch_queries_analytics."

# Test specific agent
make test-commerce INPUT="test_commerce."
```

#### **Application Management**

```bash
# Start LangGraph Studio
make studio-up

# Start FastAPI server
make api-up

# Show application status
make app-status

# View logs
make logs
```

### Query Examples

> **Note**: The examples below are in Portuguese because the system is designed to interact with users in Brazilian Portuguese, providing responses and analysis in the user's native language.

#### **Analytics Queries**

```bash
# Métricas básicas
"Quantos pedidos existem no total?"
"Qual é a receita total de vendas?"
"Qual é o valor médio do pedido?"

# Análise temporal
"Qual foi o crescimento mês a mês das vendas em 2017?"
"Calcule a taxa mensal de churn de clientes"
"Mostre as tendências de receita trimestral"

# Análise geográfica
"Quais são os 10 estados com maior receita?"
"Qual é a penetração de cada categoria por estado?"
"Quais cidades têm a maior taxa de crescimento?"

# Análise de produtos
"Identifique os 10 produtos com maior margem de contribuição"
"Quais categorias têm o maior crescimento trimestral?"
"Qual é a taxa de devolução de produtos por categoria?"
```

#### **Knowledge Queries**

```bash
# Estratégias de negócio
"Como estruturar um modelo de precificação para e-commerce?"
"Quais são as melhores práticas para retenção de clientes?"
"Como implementar gestão eficaz de estoque?"

# Insights tecnológicos
"Quais tecnologias emergentes estão impactando o e-commerce?"
"Como implementar inteligência artificial nas vendas online?"
"Quais são as últimas tendências em plataformas de e-commerce?"

# Análise de mercado
"Quais são os fatores-chave para expansão internacional?"
"Como otimizar operações de cadeia de suprimentos?"
"Quais são as melhores práticas para tomada de decisão baseada em dados?"
```

#### **Commerce Queries**

```bash
# Análise de documentos
"Analise este pedido comercial"
"Extraia informações-chave desta fatura"
"Resuma este contrato de fornecimento"
"Quais são os termos de pagamento neste documento?"

# Avaliação de risco
"Identifique riscos potenciais neste pedido"
"Quais são os problemas de conformidade neste contrato?"
"Analise as implicações financeiras deste acordo"
```

---

## Agents

### Knowledge Agent

**Purpose**: RAG system for conceptual and strategic queries

#### **Features**

- **Semantic Retrieval**: Vector-based document search using pgvector
- **Intelligent Ranking**: Heuristic re-ranking based on query overlap and relevance
- **Contextual Answering**: GPT-4o-mini powered response generation
- **Mandatory Citations**: All responses include source document references

#### **Technologies**

- **Vector Store**: pgvector with OpenAI embeddings
- **Embeddings**: text-embedding-3-small (1536 dimensions)
- **LLM**: GPT-4o-mini for response generation
- **Fallback**: Robust extractive summarization when LLM fails

#### **Knowledge Configuration**

```yaml
knowledge:
  retrieval:
    index: doc_chunks
    top_k: 5
    min_score: 0.7
  ranker:
    rerank_top_k: 3
  answerer:
    max_tokens: 2000
    require_citations: true
```

### Analytics Agent

**Purpose**: Complex SQL analysis with security and business insights

#### **Components**

##### **1. Planner**

- **Function**: Natural language to SQL translation
- **Security**: Allowlist-only table/column access
- **Examples**: 67 few-shot examples for accurate generation
- **Limits**: Automatic row caps and timeout control
- **Validation**: Schema prefix fixing and alias resolution

##### **2. Executor**

- **Function**: Safe SQL query execution
- **Security**: Read-only transactions, DDL/DML prevention
- **Timeouts**: Server-side and client-side timeout control
- **Row Limits**: Configurable row caps for large datasets

##### **3. Normalizer**

- **Function**: SQL results to Portuguese business narratives
- **LLM**: GPT-4o-mini for intelligent formatting
- **Fallback**: Robust heuristic formatting when LLM fails
- **Formatting**: Currency, percentages, tables, lists

#### **Analytics Configuration**

```yaml
analytics:
  planner:
    default_limit: 200
    max_limit: 1000
    examples_count: 3
  executor:
    default_timeout_seconds: 60
    default_row_cap: 2000
  normalizer:
    max_tokens: 2000
    timeout_seconds: 120
```

### Commerce Agent

**Purpose**: Intelligent processing of commercial documents

#### **Components**

##### **1. Processor**

- **Function**: Multi-format document text extraction
- **Formats**: DOCX, PDF, TXT, images (with OCR)
- **OCR**: Tesseract-based optical character recognition
- **Encoding**: Base64 for secure transmission

##### **2. Extractor**

- **Function**: Structured data extraction using LLM
- **Technology**: GPT-4o-mini with JSON Schema validation
- **Validation**: Consistent data structure enforcement
- **Fallback**: Robust error handling and retry mechanisms

##### **3. Summarizer**

- **Function**: Executive summary generation
- **Formatting**: Structured markdown output
- **Insights**: Risk and opportunity analysis
- **Interaction**: Follow-up question suggestions

#### **Commerce Configuration**

```yaml
commerce:
  extraction:
    min_confidence: 0.8
    json_schema_strict: true
  validation:
    line_total_tolerance: 0.01
    currency_default: "BRL"
  summarizer:
    max_tokens: 600
    top_items_display: 5
```

---

## API Reference

### REST API Endpoints

#### **Query Processing**

```http
POST /api/v1/query
Content-Type: application/json

{
  "query": "What is the total revenue?",
  "thread_id": "optional_thread_id",
  "attachment": {
    "filename": "order.pdf",
    "content": "base64_encoded_content",
    "type": "application/pdf"
  }
}
```

#### **Thread Management**

```http
# Create new thread
POST /api/v1/threads

# Get thread state
GET /api/v1/threads/{thread_id}/state

# List threads
GET /api/v1/threads
```

#### **Health Check**

```http
GET /api/v1/health
```

### LangGraph Studio API

The system exposes LangGraph Studio endpoints for advanced debugging and monitoring:

- **Studio UI**: `http://localhost:2025`
- **Graph API**: `http://localhost:2024`

---

## Development

### Project Structure

```bash

apllos-generativeai-challenge/
├── app/                          # Main application code
│   ├── agents/                   # Specialized agents
│   │   ├── analytics/            # Analytics Agent (planner, executor, normalizer)
│   │   ├── knowledge/            # Knowledge Agent (retriever, ranker, answerer)
│   │   ├── commerce/             # Commerce Agent (processor, extractor, summarizer)
│   │   └── triage/               # Triage Handler
│   ├── api/                      # REST API endpoints
│   ├── config/                   # Configuration files ()
│   ├── contracts/                # Data classes and schemas
│   ├── graph/                    # LangGraph definitions
│   ├── infra/                    # Infrastructure (db, logging, tracing)
│   ├── prompts/                  # LLM prompts and templates
│   ├── routing/                  # Routing system (classifier, supervisor)
│   └── utils/                    # Utility functions
├── data/                         # Data and documents
│   ├── docs/                     # PDF documents for RAG
│   ├── raw/                      # Raw data (CSV files)
│   └── samples/                  # Example files
├── scripts/                      # Utility scripts
│   ├── query_assistant.py        # CLI interface
│   ├── batch_query.py            # Batch processing
│   ├── ingest_analytics.py       # Data ingestion
│   ├── ingest_vectors.py         # Document ingestion
│   └── gen_allowlist.py          # Schema allowlist generation
├── tests/                        # Test suites
│   ├── unit/                     # Unit tests
│   ├── e2e/                      # End-to-end tests
│   └── batch_queries_*.      # Test query batches
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker image definition
├── Makefile                      # Automation commands
├── pyproject.toml               # Python dependencies and metadata
└── langgraph.json               # LangGraph configuration
```

### Development Commands

#### **Initial Setup**

```bash
# Install dependencies
make install-deps

# Create required directories
make dirs

# Complete bootstrap with data
make bootstrap-complete
```

#### **Development Workflow**

```bash
# Start development environment
make studio-up

# Run tests
make test

# Clean temporary files
make clean

# View logs
make logs
```

#### **Database Management**

```bash
# Reset database completely
make db-reset

# Check database status
make db-status

# Connect to database
make db-psql

# Generate allowlist
make gen-allowlist
```

#### **Data Management**

```bash
# Ingest analytics data
make ingest-analytics

# Ingest document vectors
make ingest-vectors

# Clean data directories (WARNING: deletes all data)
make clean-data
```

### Code Standards

#### **Python Standards**

- **PEP 8**: Code style guidelines
- **PEP 257**: Docstring conventions
- **Type Hints**: Full type annotation support
- **Imports**: Absolute imports with proper organization

#### **Documentation Standards**

- **Module Headers**: Standardized format with Overview, Design, Integration, Usage
- **Docstrings**: Complete documentation with Args, Returns, Raises, Examples
- **Comments**: Inline comments for complex logic
- **README**: Comprehensive project documentation

#### **Testing Standards**

- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **E2E Tests**: Full workflow testing
- **Coverage**: Maintain high test coverage

---

## Testing

### Test Structure

```bash
tests/
├── unit/                         # Unit tests
│   ├── test_analytics/           # Analytics agent tests
│   ├── test_knowledge/           # Knowledge agent tests
│   ├── test_commerce/            # Commerce agent tests
│   └── test_routing/             # Routing system tests
├── e2e/                          # End-to-end tests
│   ├── test_routing_supervisor.py
│   └── test_agent_integration.py
├── batch_queries_analytics.  # Analytics test queries
├── batch_queries_knowledge.  # Knowledge test queries
└── batch_queries_commerce.   # Commerce test queries
```

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# End-to-end tests only
make test-e2e

# System validation
make validate

# Specific test file
python -m pytest tests/unit/test_analytics/test_planner.py -v
```

### Test Data

The system includes comprehensive test datasets:

- **Analytics**: Olist e-commerce dataset with 100k+ records
- **Knowledge**: Business documents and best practices
- **Commerce**: Sample orders, invoices, and contracts

### Continuous Integration

The project supports CI/CD with automated testing:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: make install-deps
      - name: Run tests
        run: make test
```

---

## Monitoring & Observability

### Structured Logging

The system uses Python's standard `logging` with a lightweight adapter for structured context:

```python
from app.infra.logging import get_logger
logger = get_logger(__name__).bind(agent="analytics", thread_id="thread_123")
logger.info("Query processed", query="test query", duration_ms=1500, success=True)
```

### Distributed Tracing

OpenTelemetry integration for request tracing:

```python
from app.infra.tracing import get_tracer, start_span
tracer = get_tracer(__name__)
with start_span("query_processing", {"agent": "analytics"}) as span:
    span.set_attribute("query.complexity", "high")
    span.set_attribute("query.type", "revenue_analysis")
    # Process query
```

### Available Metrics

#### **Performance Metrics**

- **Query Latency**: Response time per agent and query type
- **Throughput**: Queries per minute/hour
- **Error Rate**: Error rate by component and error type
- **Resource Usage**: CPU, memory, database connections

#### **Quality Metrics**

- **Classification Accuracy**: Router decision accuracy
- **Response Quality**: User satisfaction and feedback
- **Citation Accuracy**: Knowledge agent citation relevance
- **SQL Safety**: Analytics agent security compliance

#### **Business Metrics**

- **Query Distribution**: Agent usage patterns
- **Document Processing**: Commerce agent processing success
- **User Engagement**: Query frequency and patterns
- **System Health**: Overall system availability

### Monitoring Setup

```bash
# View real-time logs
make logs

# View database logs
make logs-db

# Check system status
make app-status

# Validate system health
make validate
```

### Alerting

The system supports configurable alerting for:

- High error rates
- Performance degradation
- Resource exhaustion
- Security violations
- Data quality issues

---

## Contributing

We welcome contributions to the Apllos Generative AI Challenge project! Please follow these guidelines:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request**

### Development Guidelines

#### **Code Standards**

- Follow PEP 8 and PEP 257
- Use type hints throughout
- Write comprehensive docstrings
- Maintain test coverage above 80%

#### **Commit Messages**

Use conventional commit format:

```bash

feat: add new analytics query type
fix: resolve SQL injection vulnerability
docs: update API documentation
test: add unit tests for commerce agent
```

#### **Pull Request Process**

1. Ensure all tests pass: `make test`
2. Update documentation if needed
3. Add/update tests for new features
4. Request review from maintainers
5. Address feedback and merge

### Areas for Contribution

- **New Agent Types**: Specialized agents for different domains
- **Enhanced Security**: Additional validation and security measures
- **Performance Optimization**: Query optimization and caching
- **UI/UX Improvements**: Better user interfaces and experiences
- **Documentation**: Improved guides and examples
- **Testing**: Additional test coverage and scenarios

---

## Support

### Getting Help

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/amcerri/apllos-generativeai-challenge/issues)
- **Discussions**: Join community discussions for questions and ideas

### Troubleshooting

#### **Common Issues**

1. **Database Connection Issues**

   ```bash
   # Check database status
   make db-status
   
   # Restart database
   make db-stop && make db-start
   ```

2. **OpenAI API Issues**

   ```bash
   # Verify API key
   echo $OPENAI_API_KEY
   
   # Check API status
   curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
   ```

3. **Docker Issues**

   ```bash
   # Clean Docker environment
   make docker-reset
   
   # Rebuild and restart
   make docker-build && make studio-up
   ```

#### **Debug Mode**

Enable debug logging for troubleshooting:

```bash
LOG_LEVEL=DEBUG make query QUERY="test query"
```

## Built with LangGraph, OpenAI, and PostgreSQL
