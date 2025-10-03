# APLLOS Generative AI Challenge

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.4+-green.svg)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-20+-blue.svg)](https://docker.com)

> **Multi-Agent Intelligent System for E-commerce Data Analysis**  
> Advanced generative AI platform that combines Knowledge Retrieval, Analytics, and Commerce Processing in a unified architecture.

---

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation & Configuration](#installation--configuration)
- [Usage Guide](#usage-guide)
- [Agents](#agents)
- [Development](#development)
- [Monitoring](#monitoring)

---

## Overview

The **APLLOS Generative AI Challenge** is a generative AI platform that implements a multi-agent system specialized in e-commerce data analysis. The system combines three main agents that work in a coordinated manner to provide deep insights into commercial data.

### Key Features

- **Multi-Agent Intelligence**: Coordinated system with specialized agents
- **Advanced Analytics**: Complex SQL analysis with security and validation
- **Knowledge Retrieval**: RAG system for documents and knowledge
- **Commerce Processing**: Intelligent processing of commercial documents
- **Security**: Rigorous SQL query validation and access control
- **Observability**: Structured logging and distributed tracing
- **Containerized**: Simplified deployment with Docker

### Use Cases

- **Performance Analysis**: Sales metrics, churn rate, growth analysis
- **Product Insights**: Top products, categories, contribution margin
- **Geographic Analysis**: Performance by state, region, city
- **Document Processing**: Orders, invoices, commercial contracts
- **Business Consulting**: Questions about strategies and best practices

---

## Architecture

### Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web Interface]
        CLI[Command Line]
        API[REST API]
    end
    
    subgraph "Orchestration Layer"
        LG[LangGraph Studio]
        RT[Router & Triage]
    end
    
    subgraph "Agent Layer"
        KA[Knowledge Agent]
        AA[Analytics Agent]
        CA[Commerce Agent]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL)]
        VEC[(pgvector)]
        DOCS[Document Store]
    end
    
    subgraph "External Services"
        OAI[OpenAI API]
        EMB[Embeddings]
    end
    
    UI --> LG
    CLI --> API
    API --> RT
    RT --> KA
    RT --> AA
    RT --> CA
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
- **Function**: Request coordination and routing
- **Technology**: LangGraph 0.4+
- **Features**: Native checkpointing, persistent state

#### **2. Router & Triage System**
- **Function**: Intelligent request classification
- **Technology**: OpenAI GPT-4o-mini
- **Features**: Context and intent-based routing

#### **3. Knowledge Agent**
- **Function**: Retrieval Augmented Generation (RAG)
- **Technology**: pgvector + OpenAI Embeddings
- **Features**: Semantic search, citations, context

#### **4. Analytics Agent**
- **Function**: Complex SQL analysis and data insights
- **Technology**: PostgreSQL + SQLAlchemy
- **Features**: Security validation, LLM normalization

#### **5. Commerce Agent**
- **Function**: Commercial document processing
- **Technology**: python-docx + OCR + LLM
- **Features**: Structured extraction, intelligent summaries

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd apllos-generativeai-challenge

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your OpenAI keys

# 3. Start the complete system
make bootstrap-complete

# 4. Access LangGraph Studio
make studio-up
# Open https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
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
# Test a simple query
make query QUERY="How many orders exist in total?"

# Test with document
make query QUERY="Analyze this order" ATTACHMENT="data/samples/orders/Simple Order.docx"
```

---

## Installation & Configuration

### Prerequisites

- **Python**: 3.11+
- **Docker**: 20.0+
- **Docker Compose**: 2.0+
- **OpenAI API Key**: For LLM functionality

### Environment Configuration

#### 1. **Environment Variables**

Create a `.env` file based on `.env.example`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/apllos_db

# Application Configuration
LOG_LEVEL=INFO
DEBUG=false
```

#### 2. **Database Configuration**

```bash
# Start PostgreSQL
make db-start

# Wait for initialization
make db-wait

# Create schema and tables
make db-init

# Load sample data
make db-seed
```

#### 3. **Data Ingestion**

```bash
# Ingest analytics data (CSVs)
make ingest-analytics

# Ingest documents (PDFs)
make ingest-vectors

# Ingest everything at once
make ingest-all
```

### Docker Configuration

#### **Docker Compose**

The system uses Docker Compose for orchestration:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: apllos_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/apllos_db
    depends_on:
      - postgres
```

#### **Useful Docker Commands**

```bash
# Build image
make docker-build

# Stop all containers
make docker-stop

# Remove all containers
make docker-remove

# Clean everything (containers + images + volumes)
make docker-clean

# Complete Docker reset
make docker-reset

# View logs
make logs
```

---

## Usage Guide

### Web Interface (LangGraph Studio)

1. **Access Studio**: https://smith.langchain.com/studio/?baseUrl=http://localhost:2024
2. **Configure Thread**: Use a thread ID to maintain context
3. **Ask Questions**: Type queries in natural language
4. **Attach Documents**: For commercial document analysis

### Command Line Interface

#### **Simple Query**

```bash
make query QUERY="What is the total sales revenue?"
```

#### **Query with Thread ID**

```bash
make query QUERY="What was the growth in the last quarter?" THREAD_ID="thread_123"
```

#### **Query with Attachment**

```bash
make query QUERY="Analyze this order" ATTACHMENT="data/samples/orders/Order.docx"
```

#### **Batch Processing**

```bash
# Process multiple queries
make batch-query INPUT="tests/batch_queries_complete.yaml"

# Test commerce agent with specific input
make test-commerce INPUT="test_commerce.yaml"
```

#### **Application Management**

```bash
# Start LangGraph Studio
make studio-up

# Stop LangGraph Studio
make studio-down

# Start FastAPI server
make api-up

# Stop FastAPI server
make api-down

# Show application status
make app-status
```

### Query Examples

#### **Analytics Queries**

```bash
# Basic metrics
"How many orders exist in total?"
"What is the total sales revenue?"

# Temporal analysis
"What was the month-over-month sales growth in 2017?"
"Calculate the monthly customer churn rate"

# Geographic analysis
"What are the top 10 states by revenue?"
"What is the penetration of each category by state?"

# Product analysis
"Identify the top 10 products by contribution margin"
"Which categories have the highest quarterly growth?"
```

#### **Knowledge Queries**

```bash
# Business strategies
"How to structure a pricing model for e-commerce?"
"What are the best practices for customer retention?"

# Technologies
"What emerging technologies are impacting e-commerce?"
"How to implement artificial intelligence in online sales?"
```

#### **Commerce Queries**

```bash
# Document analysis
"Analyze this commercial order"
"Extract information from this invoice"
"Summarize this supply contract"
```

---

## Agents

### Knowledge Agent

**Function**: RAG system for conceptual and strategic queries

#### **Features**
- **Retrieval**: Semantic search in documents
- **Ranking**: Intelligent result re-ranking
- **Answering**: Contextual response generation
- **Citations**: References to source documents

#### **Technologies**
- **Vector Store**: pgvector with OpenAI embeddings
- **Embeddings**: text-embedding-3-small
- **LLM**: GPT-4o-mini for generation

#### **Configuration**
```yaml
knowledge:
  retrieval:
    index: doc_chunks
    top_k: 5
    min_score: 0.7
  answerer:
    max_citations: 3
    max_chars: 2000
```

### Analytics Agent

**Function**: Complex SQL analysis with security and insights

#### **Components**

##### **1. Planner**
- **Function**: SQL generation from natural language
- **Security**: Validation against allowlist
- **Examples**: Few-shot learning with 67 examples
- **Limits**: Row caps and timeout control

##### **2. Executor**
- **Function**: Safe SQL query execution
- **Validation**: Syntax and permission verification
- **Timeouts**: Execution time control
- **Read-only**: Data modification prevention

##### **3. Normalizer**
- **Function**: Result formatting for users
- **LLM**: GPT-4o-mini for normalization
- **Fallback**: Robust fallback system
- **Formatting**: Currency, percentages, lists

#### **Configuration**
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

**Function**: Intelligent processing of commercial documents

#### **Components**

##### **1. Processor**
- **Function**: Multi-format document processing
- **Formats**: DOCX, PDF, TXT
- **OCR**: Optical character recognition
- **Encoding**: Base64 for transmission

##### **2. Extractor**
- **Function**: Structured data extraction
- **LLM**: GPT-4o-mini with JSON Schema
- **Validation**: Consistent data structure
- **Fallback**: Robust error handling

##### **3. Summarizer**
- **Function**: Executive summary generation
- **Formatting**: Structured markdown
- **Insights**: Risk and opportunity analysis
- **Interaction**: Follow-up questions

#### **Configuration**
```yaml
commerce:
  extractor:
    model: gpt-4o-mini
    max_tokens: 4000
    temperature: 0.1
  summarizer:
    max_tokens: 600
    temperature: 0.2
```

---

## Development

### Project Structure

```
apllos-generativeai-challenge/
├── app/                          # Main code
│   ├── agents/                   # Specialized agents
│   │   ├── analytics/            # Analytics Agent
│   │   ├── knowledge/            # Knowledge Agent
│   │   ├── commerce/             # Commerce Agent
│   │   └── triage/               # Triage Handler
│   ├── api/                      # REST API
│   ├── config/                   # Configurations
│   ├── contracts/                # Data classes
│   ├── graph/                    # LangGraph definitions
│   ├── infra/                    # Infrastructure
│   ├── prompts/                  # LLM prompts
│   ├── routing/                  # Routing system
│   └── utils/                    # Utilities
├── data/                         # Data and documents
│   ├── docs/                     # PDF documents
│   ├── raw/                      # Raw data (CSV)
│   └── samples/                  # Examples
├── scripts/                      # Utility scripts
├── tests/                        # Tests
├── docker-compose.yml            # Docker Compose
├── Dockerfile                    # Docker image
├── Makefile                      # Automation commands
└── pyproject.toml               # Python dependencies
```

### Development Commands

#### **Initial Setup**
```bash
# Install dependencies
make install-deps

# Create required directories
make dirs

# Complete bootstrap
make bootstrap-complete
```

#### **Testing**
```bash
# All tests
make test

# Unit tests
make test-unit

# End-to-end tests
make test-e2e

# System validation
make validate
```

#### **Code Quality**
```bash
# Clean temporary files
make clean

# Clean data directories (WARNING: deletes CSVs and PDFs)
make clean-data
```

#### **Database**
```bash
# Complete reset
make db-reset

# Database status
make db-status

# Connect to database
make db-psql
```

#### **Bootstrap & Reset**

```bash
# Complete bootstrap: reset + minimal setup + start + ingest real data + test
make bootstrap

# GUARANTEED complete bootstrap with step-by-step data loading
make bootstrap-complete

# Complete reset: stop all + remove containers + clean volumes (keeps data)
make reset
```

#### **Utilities**

```bash
# Install/update dependencies
make install-deps

# Create required directories
make dirs

# Generate allowlist from database schema
make gen-allowlist

# Clean temporary files
make clean

# Clean data directories (WARNING: deletes CSVs and PDFs)
make clean-data

# Open shell in application container
make shell

# Open shell in database container
make shell-db
```

### Testing

#### **Available Tests**

```bash
# All tests
make test

# Unit tests
make test-unit

# End-to-end tests
make test-e2e

# System validation
make validate
```

### Logs and Debugging

#### **Logs and Debugging**

```bash
# Application logs
make logs

# Database logs
make logs-db

# Full debug
LOG_LEVEL=DEBUG make query QUERY="test"
```

#### **Tracing**

The system uses OpenTelemetry for distributed tracing:

```python
from app.infra.tracing import get_tracer

tracer = get_tracer(__name__)

@tracer.start_as_current_span("custom_operation")
def custom_function():
    # Your logic here
    pass
```

---

## Monitoring

### Available Metrics

#### **Performance**
- **Query Latency**: Response time per agent
- **Throughput**: Queries per minute
- **Error Rate**: Error rate per component

#### **Quality**
- **Classification Accuracy**: Routing precision
- **Response Quality**: Response quality
- **User Satisfaction**: User feedback

#### **Resources**
- **Database Connections**: Connection pool
- **Memory Usage**: Memory consumption
- **CPU Usage**: CPU utilization

### Observability

#### **Structured Logging**

```python
from app.infra.logging import get_logger

logger = get_logger(__name__)

logger.info("Query processed", 
    query="test query",
    agent="analytics",
    duration_ms=1500,
    success=True
)
```

#### **Distributed Tracing**

```python
from app.infra.tracing import get_tracer

tracer = get_tracer(__name__)

with tracer.start_as_current_span("query_processing") as span:
    span.set_attribute("query.type", "analytics")
    span.set_attribute("query.complexity", "high")
    # Query processing
```

