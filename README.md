# apllos-generativeai-challenge

Assistente de engenharia baseado em **LangGraph** que roteia solicitações do usuário entre quatro agentes especializados — **analytics**, **knowledge**, **commerce** e **triage** — e responde ao usuário final em **pt-BR**. O runtime oferece persistência (checkpointer), interrupções *human‑in‑the‑loop*, *logging* estruturado e *tracing* opcional.

---

## Visão geral
Este projeto implementa um **roteador "context‑first"** + quatro agentes:

- **analytics** — SQL seguro sobre dados de analytics do Olist (apenas allowlist; sem `SELECT *`; `LIMIT` obrigatório em *preview*). A resposta final é humanizada/negócio em pt‑BR.
- **knowledge** — RAG com pgvector; quando usa recuperação **sempre cita as fontes** (título + id/URL + linhas).
- **commerce** — documentos comerciais heterogêneos (PO/Order Form/BEO/invoice etc.) → **schema canônico** (buyer/vendor/items/totals/terms/signatures/risks) + resumo em pt‑BR.
- **triage** — orientação breve e redirecionamento quando o contexto é insuficiente.

**Regras de roteamento (com *fallback* de uma passagem; sem loops):**
1. Se respondível por documentos → **knowledge**.
2. Se envolver tabelas/colunas/medidas/agrupamentos → **analytics**.
3. Se houver indícios de documento comercial → **commerce**.
4. Caso contrário → **triage**.

**Modelos (OpenAI apenas):** roteador `gpt-4.1-mini`; *analytics planner* `o3` (ou `o4-mini`); RAG `gpt-4.1` (ou `gpt-4.1-mini`); *commerce extractor* `gpt-4.1`.

**Contratos (dataclasses):**
- `RouterDecision`: `{ agent ∈ {analytics,knowledge,commerce,triage}, confidence, reason, tables[], columns[], signals[], thread_id? }`.
- `Answer`: `{ text, data?, columns?, citations?, meta?, no_context?, artifacts?, followups? }`.

---

## Arquitetura
- **LangGraph** orquestra o grafo (nós = agentes/etapas do pipeline).
- **LangGraph Server + Studio** expõem endpoints HTTP/stream e UI visual. O Server importa `app.graph.assistant:get_assistant`.
- **Postgres** (com **pgvector**) armazena dados tabulares e embeddings de documentos.
- **Checkpointer** persiste estado/thread para retomada.
- **Observabilidade**: `structlog` (campos `component`/`event`/`thread_id`) e spans opcionais via OpenTelemetry.
- **Config**: `app/config/config.yaml` (ex.: `confidence_min`, `retrieval_min_score`, *timeouts* e *row caps*) e `app/config/models.yaml` (nomes dos modelos).

**Estrutura (resumo):**

```text
app/                # agents, routing, contracts, prompts, api, config, graph, infra, utils
├── agents/         # 4 agentes especializados (analytics, knowledge, commerce, triage)
├── api/            # FastAPI server
├── config/         # configurações YAML
├── contracts/      # dataclasses de resposta
├── graph/          # LangGraph assembly e assistant factory
├── infra/          # logging, tracing, db, checkpointer
├── prompts/        # prompts organizados por agente
├── routing/        # LLM classifier e supervisor
└── utils/          # utilitários (ids, time, validation, typing)
scripts/            # ingest_analytics.py, ingest_vectors.py, explain_sql.py, gen_allowlist.py
data/raw/analytics # CSVs do Olist (NÃO versionados)
data/docs/         # PDFs/TXT para RAG (NÃO versionados)
```

---

## Requisitos
- **Python 3.11+**
- **Docker** + **Docker Compose**
- **GNU Make**

> Dica: os *targets* do Make já encapsulam os comandos Docker e utilitários comuns.

---

## Configuração de ambiente
1) Crie seu arquivo `.env` a partir do exemplo:
```bash
cp .env.example .env
```

2) Preencha as variáveis principais (exemplo):
```dotenv
# OpenAI (obrigatório para ingestão de vetores e execução de LLMs)
OPENAI_API_KEY=sk-...

# Postgres (Makefile também define defaults)
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=app
POSTGRES_PORT=5432

DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
LANGGRAPH_DEV_CONFIG=langgraph.json
```

> **Nota:** se você **não** estiver usando Docker/Compose e rodar a API localmente, use `localhost` no `DATABASE_URL`:
```dotenv
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app
```

---

## Primeiros passos (modo Docker‑first)
Os comandos abaixo sobem o Postgres (com pgvector), preparam o schema mínimo e deixam tudo pronto para ingestão e execução.

```bash
# 1) Criar pastas de dados
make dirs

# 2) Subir Postgres + esperar ficar pronto + inicializar extensões/roles/db
make db-start db-wait db-init

# 3) (Opcional) Popular amostras mínimas de schema/dados
make db-seed   # usa data/samples/schema.sql e data/samples/seed.sql

# 4) (Quando o Dockerfile existir) build e run da imagem
make app-build
make app-run CMD="python -m app.graph.assistant"
```

> Você pode inspecionar ajuda dos *targets* com `make help`.

---

## Executar LangGraph Studio (via Docker Compose)
O fluxo recomendado para desenvolvimento visual é rodar o **LangGraph Dev Server** dentro do container e abrir o Studio no navegador.

```bash
# Banco de dados ativo (se ainda não estiver rodando)
make db-start db-wait db-init

# Sobe o Dev Server (exporá a API e abrirá o Studio)
make studio-compose
```

- API: `http://127.0.0.1:2024`
- Studio UI: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`
- Docs (OpenAPI): `http://127.0.0.1:2024/docs`

> Observação: versões recentes do CLI usam `langgraph dev` (e **não** `langgraph server`). O `make studio-compose` já usa o modo correto e injeta `LANGGRAPH_SERVER_APP="app.graph.assistant:get_assistant"`.

---

## Ingestão — Analytics (CSV → Postgres)
1) Coloque os CSVs do Olist em `data/raw/analytics/` (não versionados neste repositório).

2) Execute o *script* de ingestão:
```bash
python scripts/ingest_analytics.py --help
python scripts/ingest_analytics.py \
  --dsn "$DATABASE_URL" \
  --csv-root data/raw/analytics \
  --schema-sql data/samples/schema.sql
```

3) (Opcional) Gere um **allowlist** a partir do schema ativo (para o planner SQL):
```bash
python scripts/gen_allowlist.py --help
python scripts/gen_allowlist.py --dsn "$DATABASE_URL" --out app/routing/allowlist.json
```

> O agente **analytics** NUNCA usa colunas/tabelas fora do allowlist.

---

## Ingestão — Knowledge (RAG com pgvector)
1) Coloque PDFs/TXT em `data/docs/`.

2) Gere embeddings e upsert no Postgres/pgvector:
```bash
python scripts/ingest_vectors.py --help
python scripts/ingest_vectors.py \
  --dsn "$DATABASE_URL" \
  --docs-root data/docs \
  --model $(yq '.embeddings_model' app/config/models.yaml)
```

> Requer `OPENAI_API_KEY`. O script cria/atualiza índices (HNSW/IVFFlat) conforme disponível.

---

## Execução
Há duas formas principais: **API FastAPI** ou **LangGraph Server + Studio**.

### 1) API (FastAPI)
```bash
# inicia a API (hot-reload em desenvolvimento)
uvicorn app.api.server:get_app --reload --port 8000
```
Abra `http://localhost:8000/docs` para explorar os endpoints.

### 2) LangGraph Server + Studio
O Server importa `app.graph.assistant:get_assistant`.

```bash
# se o CLI do LangGraph estiver instalado
export LANGGRAPH_SERVER_APP="app.graph.assistant:get_assistant"
# CLI recente: use o modo "dev"
langgraph dev --config langgraph.json --host 0.0.0.0 --port 2024
```

> Alternativamente, alguns setups aceitam: `python -m app.graph.assistant` para validar a compilação do grafo.

### Gate de aprovação (Human‑in‑the‑loop)
- Por padrão, `require_sql_approval: true` (ver `config.yaml`).
- O nó de *analytics* pode pausar antes de executar SQL; aprove o *gate* pelo Server/Studio ou desabilite (defina `require_sql_approval=false`).

---

## Testes
Executa unitários + e2e:
```bash
pytest -q
```
Rode seleções específicas:
```bash
pytest tests/unit -q
pytest tests/e2e -q
```

---

## Observabilidade
- **Logging**: `structlog` com chaves `component`, `event`, `thread_id` em todos os nós.
- **Tracing (opcional)**: spans por nó via OpenTelemetry (configure `OTEL_EXPORTER_OTLP_ENDPOINT`).

---

## Convenções de código e *prompts*
- **Idioma**: código em **inglês**; respostas de runtime (Answer.text) em **pt‑BR**.
- **Estilo**: PEP‑8, PEP‑257, *type hints* completos.
- **Documentação**: Headers padronizados com Overview/Design/Integration/Usage em todos os módulos.
- **Prompts versionados** em `app/prompts/**` (routing, analytics, knowledge, commerce).
- **Arquivos temporários**: Removidos todos os arquivos de debug e fallbacks antigos.

---

## Segurança & *guardrails*
- **Analytics**: *allowlist‑only*, somente leitura, sem DDL/DML, **sem** `SELECT *`, `LIMIT` obrigatório em *preview*.
- **Knowledge**: nunca inventa base inexistente; **citações obrigatórias** quando usa RAG; se *retrieval* fraco → `no_context=true` + *follow‑ups*.
- **Commerce**: normaliza moeda/datas/quantidades; checagem de soma de linhas ≈ subtotal; campos opcionais de *risks/warnings*.

---

## Fluxos ponta‑a‑ponta (resumo)
**A. Setup e ingestão**
```bash
make dirs
make db-start db-wait db-init db-seed
python scripts/ingest_analytics.py --dsn "$DATABASE_URL" --csv-root data/raw/analytics --schema-sql data/samples/schema.sql
python scripts/ingest_vectors.py --dsn "$DATABASE_URL" --docs-root data/docs
python scripts/gen_allowlist.py --dsn "$DATABASE_URL" --out app/routing/allowlist.json
```

**B. Execução**
```bash
uvicorn app.api.server:get_app --reload --port 8000
# ou
export LANGGRAPH_SERVER_APP="app.graph.assistant:get_assistant" && langgraph server
```

**C. Testes**
```bash
pytest -q
```

---

## Make — atalhos úteis
- `make dirs` — cria `data/raw/analytics` e `data/docs`
- `make db-start` / `make db-wait` / `make db-init` — sobe e prepara o Postgres (pgvector)
- `make db-seed` — aplica `data/samples/schema.sql` e `data/samples/seed.sql`
- `make ingest-analytics` — carrega CSVs do Olist (ordem segura para FKs)
- `make ingest-vectors` — indexa documentos em pgvector
- `make gen-allowlist` — gera allowlist a partir do schema atual
- `make studio-compose` — inicia LangGraph Dev Server (API + Studio)
- `make studio-down` — encerra a sessão do Studio
- `make compose-down` — derruba containers e volumes (cuidado)

---

## Limpeza e Padronização
O projeto passou por uma limpeza completa e padronização:

### ✅ **Arquivos Removidos**
- `get_full_response.py` - script de debug temporário
- `test_api.py` - teste temporário  
- `test_queries.sh` - script de teste temporário
- `app/agents/analytics/*_simple.py` - versões fallback antigas
- `app/routing/allowlist_snapshot.py` - snapshot temporário

### ✅ **Padronização Aplicada**
- **Headers uniformes**: Todos os módulos seguem o padrão Overview/Design/Integration/Usage
- **PEP8/PEP257**: Código totalmente conforme com docstrings completas
- **Organização**: Estrutura de diretórios clara e lógica
- **Documentação**: Comentários em inglês, respostas em PT-BR
- **Zero erros**: Linting e compilação sem problemas

### ✅ **Estrutura Final**

```text
app/
├── agents/         # 4 agentes especializados
├── api/            # FastAPI server
├── config/         # configurações YAML
├── contracts/      # dataclasses de resposta
├── graph/          # LangGraph assembly
├── infra/          # logging, tracing, db
├── prompts/        # prompts organizados
├── routing/        # LLM classifier e supervisor
└── utils/          # utilitários
```

---

## *Troubleshooting*
- **Studio 400 / `InvalidUpdateError: ... Can receive only one value per step`**: garanta que cada nó do grafo escreva **apenas um** valor por passo na mesma chave; no projeto já ajustamos isso em `app/graph/build.py`.
- **LangGraph: "No such command 'server'"**: use `langgraph dev --config langgraph.json`. Os alvos do Make já fazem isso para você.
- **Studio URL com 0.0.0.0**: substitua `0.0.0.0` por `localhost` na URL do Studio (ex: `http://localhost:2024`).
- **Ruff UP038**: troque `isinstance(x, (A, B))` por `isinstance(x, A | B)`.
- **mypy: Unused "type: ignore"**: remova comentários supérfluos; tipagem foi ajustada nos módulos.
- **Falta do pgvector**: garanta que `make db-init` rodou (criação da extensão); verifique logs do container.
- **OPENAI_API_KEY ausente**: embeddings/LLM falharão; defina no `.env`.
- **Permissões de arquivo CSV**: confira `data/raw/analytics` e *paths* passados aos scripts.
- **Arquivos temporários**: Todos os arquivos de debug e fallbacks antigos foram removidos na limpeza.
