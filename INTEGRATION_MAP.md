# Mapa de Integrações e Fluxo de Dados - Apllos Assistant

## Visão Geral da Arquitetura

O sistema é um **assistente multi-agente baseado em LangGraph** que processa diferentes tipos de dados através de agentes especializados:

- **Analytics Agent**: Análise de dados tabulares (SQL)
- **Knowledge Agent**: Busca semântica em documentos (RAG)
- **Commerce Agent**: Processamento de documentos comerciais
- **Triage Agent**: Direcionamento e orientação

## Fluxo Principal de Dados

### 1. Entrada (Input Layer)
```
User Query/Attachment → API Server → LangGraph Graph
```

**Componentes:**
- `app/api/server.py`: FastAPI server com CORS
- `app/graph/assistant.py`: Entry point do LangGraph
- `app/graph/build.py`: Construção do grafo de workflow

### 2. Roteamento (Routing Layer)
```
Query → LLMClassifier → Supervisor → Agent Selection
```

**Componentes:**
- `app/routing/llm_classifier.py`: Classificação LLM com fallback heurístico
- `app/routing/supervisor.py`: Regras de supervisão e fallbacks
- `app/routing/allowlist.json`: Lista de tabelas/colunas permitidas

**Fluxo:**
1. **LLMClassifier** analisa query + allowlist
2. **Supervisor** aplica regras determinísticas
3. **RouterDecision** é criado com agente, confiança e razão

### 3. Processamento por Agente

#### Analytics Agent
```
Query → Planner → Executor → Normalizer → Answer
```

**Componentes:**
- `app/agents/analytics/planner.py`: Geração de SQL seguro
- `app/agents/analytics/executor.py`: Execução com timeouts/limits
- `app/agents/analytics/normalize.py`: Normalização para português

**Fluxo:**
1. **Planner** gera SQL usando LLM + allowlist
2. **Executor** executa com transações read-only
3. **Normalizer** converte resultados para narrativa PT-BR

#### Knowledge Agent
```
Query → Retriever → Ranker → Answerer → Answer
```

**Componentes:**
- `app/agents/knowledge/retriever.py`: Busca vetorial (pgvector)
- `app/agents/knowledge/ranker.py`: Re-ranking heurístico
- `app/agents/knowledge/answerer.py`: Composição de resposta

**Fluxo:**
1. **Retriever** busca chunks relevantes via embedding
2. **Ranker** re-ordena por relevância
3. **Answerer** compõe resposta com citações

#### Commerce Agent
```
Attachment → Processor → Extractor → Summarizer → Answer
```

**Componentes:**
- `app/agents/commerce/processor.py`: Extração de texto (PDF/DOCX/OCR)
- `app/agents/commerce/extractor.py`: Extração estruturada (heurística)
- `app/agents/commerce/extractor_llm.py`: Extração via LLM
- `app/agents/commerce/summarizer.py`: Resumo em português

**Fluxo:**
1. **Processor** extrai texto de documentos
2. **Extractor** estrutura dados (LLM ou heurística)
3. **Summarizer** gera resumo executivo

#### Triage Agent
```
Query → TriageHandler → Answer
```

**Componentes:**
- `app/agents/triage/handler.py`: Direcionamento e orientação

## Integrações Críticas

### 1. Sistema de Configuração
**Arquivo:** `app/config/loader.py`
**Dependências:**
- `config.yaml`: Configuração geral
- `agents.yaml`: Configurações dos agentes
- `models.yaml`: Configurações dos LLMs
- `database.yaml`: Configuração do banco
- `observability.yaml`: Logging e tracing

**Pontos Críticos:**
- Substituição de variáveis de ambiente `${VAR:-default}`
- Merge recursivo de configurações
- Acesso tipado via `get()` com dot notation

### 2. Contratos de Dados
**Arquivos:** `app/contracts/answer.py`, `app/contracts/router_decision.py`

**Pontos Críticos:**
- **Answer**: Contrato unificado para todas as respostas
- **RouterDecision**: Contrato para decisões de roteamento
- Validação rigorosa com JSON Schema
- Campos obrigatórios vs opcionais

### 3. Infraestrutura de Banco
**Arquivo:** `app/infra/db.py`
**Dependências:**
- SQLAlchemy engine global
- PostgreSQL com pgvector
- Pool de conexões configurável
- Transações read-only por padrão

**Pontos Críticos:**
- Configuração global única (`_ENGINE`)
- Lazy initialization
- Context manager para conexões

### 4. Sistema de Logging
**Arquivo:** `app/infra/logging.py`
**Dependências:**
- structlog para logging estruturado
- Configuração via YAML
- Fallback para logging padrão

### 5. Sistema de Tracing
**Arquivo:** `app/infra/tracing.py`
**Dependências:**
- OpenTelemetry (opcional)
- Fallback para nullcontext
- Configuração de exporters

### 6. Checkpointer
**Arquivo:** `app/infra/checkpointer.py`
**Dependências:**
- LangGraph PostgresSaver
- Fallback para NoopSaver
- Configuração via environment

## Fluxo de Dados Detalhado

### 1. Inicialização do Sistema
```
1. ConfigLoader.load() → merge YAML files
2. configure_engine() → setup PostgreSQL
3. configure_logging() → setup structlog
4. configure_tracing() → setup OpenTelemetry
5. get_assistant() → compile LangGraph
```

### 2. Processamento de Query
```
1. API receives request
2. LangGraph creates thread
3. Router classifies query
4. Supervisor applies rules
5. Agent processes request
6. Answer is returned
```

### 3. Human-in-the-Loop
```
1. SQL execution requires approval
2. HumanGate interrupts workflow
3. User approves/rejects
4. Workflow continues
```

## Dependências Externas

### 1. OpenAI
- **Uso:** LLM para todos os agentes
- **Configuração:** `OPENAI_API_KEY`
- **Modelos:** gpt-4o-mini (padrão)
- **Fallbacks:** Heurísticas quando LLM falha

### 2. PostgreSQL + pgvector
- **Uso:** Analytics data + RAG embeddings
- **Configuração:** `DATABASE_URL`
- **Extensões:** vector, pg_stat_statements
- **Índices:** HNSW para busca vetorial

### 3. Document Processing
- **PyPDF:** Extração de PDF
- **python-docx:** Processamento DOCX
- **pytesseract:** OCR para imagens
- **pdf2image:** Conversão PDF→imagem

## Pontos Críticos de Integração

### 1. **ConfigLoader** → **Todos os Módulos**
- **Risco:** Mudança na estrutura de config quebra todos os agentes
- **Mitigação:** Versionamento de config, fallbacks

### 2. **Answer Contract** → **Todos os Agentes**
- **Risco:** Mudança no contrato quebra compatibilidade
- **Mitigação:** Versionamento de contratos, validação rigorosa

### 3. **Database Engine** → **Analytics + Knowledge**
- **Risco:** Mudança na configuração quebra ambos os agentes
- **Mitigação:** Configuração global única, lazy initialization

### 4. **LLM Backend** → **Todos os Agentes**
- **Risco:** Falha do LLM quebra todos os agentes
- **Mitigação:** Fallbacks heurísticos, retry logic

### 5. **LangGraph State** → **Workflow**
- **Risco:** Mudança no estado quebra o workflow
- **Mitigação:** TypedDict com Annotated reducers

## Scripts de Ingestão

### 1. **ingest_analytics.py**
- **Função:** Carrega dados CSV para PostgreSQL
- **Dependências:** SQLAlchemy, PostgreSQL
- **Fluxo:** CSV → COPY → Analytics Schema

### 2. **ingest_vectors.py**
- **Função:** Cria embeddings de documentos
- **Dependências:** OpenAI, pgvector
- **Fluxo:** PDF/TXT → Chunks → Embeddings → pgvector

### 3. **gen_allowlist.py**
- **Função:** Gera allowlist do schema
- **Dependências:** PostgreSQL
- **Fluxo:** Schema → Tables/Columns → allowlist.json

## Monitoramento e Observabilidade

### 1. **Logging Estruturado**
- **Componente:** `app.infra.logging`
- **Formato:** JSON ou console
- **Contexto:** Component name + initial values

### 2. **Distributed Tracing**
- **Componente:** `app.infra.tracing`
- **Backend:** OpenTelemetry
- **Spans:** Por operação (agent, LLM, DB)

### 3. **Health Checks**
- **Endpoint:** `/health`, `/ready`
- **Verificações:** DB connection, LLM availability

## Considerações de Performance

### 1. **Database**
- **Pool:** Configurável (padrão: 10 conexões)
- **Timeouts:** Statement timeout, connection timeout
- **Read-only:** Transações por padrão

### 2. **LLM Calls**
- **Retry:** Configurável (padrão: 3 tentativas)
- **Timeout:** Por modelo (10-120s)
- **Caching:** Via LangGraph checkpointer

### 3. **Vector Search**
- **Index:** HNSW para performance
- **Batch:** Embeddings em lote
- **Deduplication:** Por doc_id

## Segurança

### 1. **SQL Injection**
- **Mitigação:** Allowlist de tabelas/colunas
- **Validação:** SQL parsing + allowlist check
- **Execução:** Read-only transactions

### 2. **File Processing**
- **Limites:** Tamanho máximo, páginas máximas
- **Formato:** Validação de MIME type
- **OCR:** Configuração de idioma

### 3. **API Security**
- **CORS:** Configurável
- **Rate Limiting:** Via LangGraph
- **Authentication:** Não implementado (explicit)

## Conclusão

O sistema é altamente modular com **dependências bem definidas** e **fallbacks robustos**. Os pontos críticos são:

1. **ConfigLoader** como fonte única de verdade
2. **Answer Contract** como interface unificada
3. **Database Engine** como infraestrutura compartilhada
4. **LLM Backend** como dependência crítica

A arquitetura permite **evolução incremental** com **baixo acoplamento** entre módulos, mas requer **cuidado especial** ao modificar os pontos críticos de integração.
