# Examples and Use Cases: Practical Applications

This document provides examples and use cases for the Apllos Assistant system.

## Use Cases Overview

The Apllos Assistant supports these main use cases:

- **Analytics Queries**: Natural language to SQL conversion for e-commerce data
- **Knowledge Retrieval**: Document search and information synthesis
- **Commerce Processing**: Document processing and data extraction
- **Query Routing**: Intelligent routing to appropriate agents

## Analytics Examples

### 1. Sales Analysis
**Query**: "Quantos pedidos existem no total?"
**Agent**: Analytics
**Response**: SQL query execution with total order count

### 2. Customer Analysis
**Query**: "Qual a receita total?"
**Agent**: Analytics
**Response**: SQL query execution with total revenue

### 3. Geographic Analysis
**Query**: "Detalhe por estado"
**Agent**: Analytics
**Response**: SQL query execution with state-wise breakdown

## Knowledge Examples

### 1. Document Search
**Query**: "Quais são as melhores práticas de precificação no e-commerce?"
**Agent**: Knowledge (RAG)
**Response**: Document retrieval and synthesis from knowledge base

### 2. Information Retrieval
**Query**: "Como funciona o processo de entrega?"
**Agent**: Knowledge (RAG)
**Response**: Document-based answer with citations

## Commerce Examples

### 1. Document Processing
**Query**: "Analise este pedido"
**Attachment**: Document file (PDF, DOCX, TXT)
**Agent**: Commerce
**Response**: Document processing and structured data extraction

### 2. Invoice Analysis
**Query**: "Analise esta fatura"
**Attachment**: Invoice document
**Agent**: Commerce
**Response**: Invoice data extraction and analysis

## Usage Examples

### CLI Usage
```bash
# Analytics query
make query QUERY="Quantos pedidos existem no total?"

# Knowledge query
make query QUERY="Quais são as melhores práticas de precificação no e-commerce?"

# Commerce query with attachment
make query QUERY="Analise este pedido" ATTACHMENT="data/samples/orders/Simple Order.docx"

# Reuse thread for context
make query QUERY="Detalhe por estado" THREAD_ID=thr-...
```

### LangGraph Studio
- Access: `https://smith.langchain.com/studio/?baseUrl=http://localhost:2024`
- Features: Visual graph execution, thread management, debugging

### API Usage
```bash
# Health check
curl http://localhost:2024/ok

# Metrics (if prometheus_client installed)
curl http://localhost:2024/metrics
```

## Data Examples

### Analytics Data
- **Orders**: Order information and transactions
- **Customers**: Customer profiles and demographics
- **Products**: Product catalog and categories
- **Sellers**: Seller information and performance
- **Reviews**: Customer reviews and ratings

### Knowledge Data
- **Documents**: PDF e-books and guides
- **Content**: E-commerce best practices and tutorials
- **Embeddings**: Vector embeddings for semantic search

### Commerce Data
- **Sample Documents**: Invoice, purchase order, receipt samples
- **Processing**: Multi-format document processing
- **Extraction**: Structured data extraction

## Agent Routing Examples

### Analytics Routing
- Queries about data, metrics, analysis
- Keywords: "quantos", "receita", "vendas", "análise"

### Knowledge Routing
- Queries about information, processes, best practices
- Keywords: "como", "quais", "melhores práticas", "processo"

### Commerce Routing
- Queries with document attachments
- Keywords: "analise", "processe", "extraia"

### Triage Routing
- Ambiguous or unclear queries
- Insufficient context for routing

## Configuration Examples

### Environment Variables
```bash
OPENAI_API_KEY=your-key-here
DATABASE_URL=postgresql://app:app@localhost:5432/app
LOG_LEVEL=INFO
REQUIRE_SQL_APPROVAL=false
```

### Model Configuration
```yaml
models:
  router:
    model: gpt-4o-mini
  analytics_planner:
    model: gpt-4o-mini
  knowledge_answerer:
    model: gpt-4o-mini
```

## Troubleshooting Examples

### Common Issues
```bash
# Database connection
make db-status
make db-stop && make db-start

# OpenAI API
echo $OPENAI_API_KEY

# Application logs
make logs

# Health check
curl http://localhost:2024/ok
```

This examples guide provides practical examples based on the actual Apllos Assistant implementation.
---

**← [Back to Documentation Index](../README.md)**
