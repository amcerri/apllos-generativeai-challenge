# Agents Overview: Complete System Guide

This document provides a comprehensive overview of all agents in the Apllos Assistant system, their interactions, and how they work together to provide intelligent assistance.

## Agent Architecture

The Apllos Assistant uses a multi-agent architecture where each agent specializes in a specific domain:

```
User Query   →   Router   →   Supervisor   →   Agent   →   LLM   →   Database   →   Response
     ↓             ↓              ↓              ↓          ↓           ↓              ↓
  Input         Decision     Guardrails     Specialized   OpenAI    PostgreSQL       PT-BR
                 Making      & Fallbacks    Processing     API      + pgvector       Output
```

## Agent Specializations

### 1. Analytics Agent
**Purpose**: Converts natural language queries into safe SQL and provides data analysis

**Components**:
- **Planner**: Converts NL to SQL with allowlist validation
- **Executor**: Safely executes SQL with read-only transactions
- **Normalizer**: Converts raw data to PT-BR narratives

**Key Features**:
- Allowlist-based SQL generation
- Read-only transaction safety
- Intelligent data balancing
- Human approval gates for SQL execution
- Circuit breaker for repeated failures

**Use Cases**:
- "Quantos pedidos existem no total?"
- "Mostre os produtos mais vendidos"
- "Qual a receita por mês?"

### 2. Knowledge Agent (RAG)
**Purpose**: Retrieves and synthesizes information from document knowledge base

**Components**:
- **Retriever**: Vector search using pgvector embeddings
- **Ranker**: Ranks documents by relevance (heuristic + optional LLM)
- **Answerer**: Generates answers with citations and cross-validation

**Key Features**:
- Vector similarity search with pgvector
- Document deduplication and ranking
- Cross-validated responses with citations
- Fallback to extractive summarization
- Confidence calibration for answers

**Use Cases**:
- "Como funciona o e-commerce?"
- "Quais são as melhores práticas de vendas?"
- "Explique sobre embalagens para e-commerce"

### 3. Commerce Agent
**Purpose**: Processes commercial documents and extracts structured data

**Components**:
- **Processor**: Multi-format document extraction (PDF/DOCX/TXT/OCR)
- **Extractor**: Structured data extraction with LLM
- **Summarizer**: Executive summaries with risk analysis

**Key Features**:
- Multi-format document processing
- OCR fallback for scanned documents
- Structured data extraction with validation
- Risk analysis and flagging
- Executive summary generation

**Use Cases**:
- Process invoices and receipts
- Extract order information
- Analyze commercial documents
- Generate risk assessments

### 4. Triage Agent
**Purpose**: Handles ambiguous queries and provides guidance

**Components**:
- **Handler**: Analyzes query context and provides guidance
- **Fallback Logic**: Suggests appropriate agents
- **User Guidance**: Provides follow-up questions

**Key Features**:
- Context analysis and guidance
- Agent suggestion based on signals
- Follow-up question generation
- Safe fallback for ambiguous queries

**Use Cases**:
- Ambiguous or unclear queries
- Insufficient context for routing
- User guidance and assistance

## Agent Interactions

### Routing Flow
1. **User Query** → Router analyzes intent and context
2. **Router Decision** → Supervisor applies guardrails
3. **Final Decision** → Routes to appropriate agent
4. **Agent Processing** → Specialized pipeline execution
5. **Response Generation** → PT-BR response with metadata

### Inter-Agent Communication
- **Shared State**: GraphState with per-agent channels
- **Context Passing**: Routing context and signals
- **Error Handling**: Graceful degradation and fallbacks
- **Monitoring**: Metrics and observability across agents

## Agent Capabilities Matrix

| Capability | Analytics | Knowledge | Commerce | Triage |
|------------|-----------|-----------|----------|--------|
| **SQL Generation** | ✅ | ❌ | ❌ | ❌ |
| **Data Analysis** | ✅ | ❌ | ❌ | ❌ |
| **Document Retrieval** | ❌ | ✅ | ❌ | ❌ |
| **Document Processing** | ❌ | ❌ | ✅ | ❌ |
| **Structured Extraction** | ❌ | ❌ | ✅ | ❌ |
| **User Guidance** | ❌ | ❌ | ❌ | ✅ |
| **Fallback Handling** | ❌ | ❌ | ❌ | ✅ |
| **Citations** | ❌ | ✅ | ❌ | ❌ |
| **Risk Analysis** | ❌ | ❌ | ✅ | ❌ |

## Agent Configuration

### Analytics Agent
```yaml
analytics:
  planner:
    default_limit: 200
    max_limit: 1000
    enforce_limit: true
  executor:
    read_only: true
    timeout: 120
    max_rows: 10000
  normalizer:
    complete_data_threshold: 100
    enable_llm: true
```

### Knowledge Agent
```yaml
knowledge:
  retrieval:
    top_k: 7
    min_score: 0.7
    dedupe: true
  ranker:
    rerank_top_k: 3
    enable_llm: false
  answerer:
    max_tokens: 2000
    require_citations: true
```

### Commerce Agent
```yaml
commerce:
  extraction:
    min_confidence: 0.8
    json_schema_strict: true
  validation:
    line_total_tolerance: 0.01
    default_currency: "BRL"
  summarizer:
    max_items: 10
    include_risks: true
```

### Triage Agent
```yaml
triage:
  handler:
    max_suggestions: 3
    include_followups: true
  fallback:
    enable_guidance: true
    suggest_agents: true
```

## Agent Performance Metrics

### Analytics Agent
- **SQL Generation Time**: Average time to generate SQL
- **Execution Time**: Average time to execute queries
- **Accuracy**: Percentage of correct SQL generation
- **Safety**: Number of blocked unsafe queries

### Knowledge Agent
- **Retrieval Time**: Average time to retrieve documents
- **Relevance Score**: Average relevance of retrieved documents
- **Answer Quality**: User satisfaction with answers
- **Citation Accuracy**: Percentage of accurate citations

### Commerce Agent
- **Processing Time**: Average time to process documents
- **Extraction Accuracy**: Percentage of correctly extracted data
- **Risk Detection**: Number of risks identified
- **Summary Quality**: User satisfaction with summaries

### Triage Agent
- **Guidance Quality**: User satisfaction with guidance
- **Agent Suggestions**: Accuracy of agent recommendations
- **Fallback Usage**: Frequency of fallback scenarios
- **User Engagement**: Follow-up question effectiveness

## Agent Development Guidelines

### Adding New Agents
1. **Create Agent Module**: `app/agents/new_agent/`
2. **Implement Pipeline**: Follow existing patterns
3. **Add Routing Logic**: Update router and supervisor
4. **Configure Settings**: Add to `agents.yaml`
5. **Write Tests**: Unit and integration tests
6. **Update Documentation**: Agent-specific docs

### Agent Best Practices
- **Single Responsibility**: Each agent has one clear purpose
- **Graceful Degradation**: Fallback when LLM unavailable
- **Safety First**: Validate inputs and outputs
- **Observability**: Comprehensive logging and metrics
- **Testing**: Thorough test coverage
- **Documentation**: Clear and comprehensive docs

## Troubleshooting Common Issues

### Analytics Agent Issues
- **SQL Generation Errors**: Check allowlist and prompts
- **Execution Timeouts**: Adjust timeout settings
- **Data Quality**: Validate input data and schema
- **Performance**: Optimize queries and indexes

### Knowledge Agent Issues
- **Retrieval Quality**: Check embeddings and vector index
- **Citation Accuracy**: Validate document sources
- **Answer Quality**: Review prompts and examples
- **Performance**: Optimize vector search

### Commerce Agent Issues
- **Document Processing**: Check OCR and format support
- **Extraction Accuracy**: Validate prompts and examples
- **Risk Detection**: Review risk analysis logic
- **Summary Quality**: Check summarization prompts

### Triage Agent Issues
- **Guidance Quality**: Review guidance prompts
- **Agent Suggestions**: Validate routing logic
- **Fallback Logic**: Check fallback scenarios
- **User Experience**: Improve guidance clarity

## Future Enhancements

### Planned Improvements
- **Multi-Modal Support**: Images and documents
- **Advanced Analytics**: Statistical analysis and ML
- **Real-Time Processing**: Streaming data analysis
- **Custom Agents**: User-defined agent creation
- **Agent Collaboration**: Inter-agent communication
- **Learning**: Adaptive behavior based on usage

### Research Areas
- **Agent Orchestration**: Advanced coordination patterns
- **Context Awareness**: Better context understanding
- **Personalization**: User-specific agent behavior
- **Automation**: Reduced human intervention
- **Scalability**: High-performance agent execution

This comprehensive overview should help developers understand the complete agent system and how to work with it effectively.

---

**← [Back to Documentation Index](../README.md)**
