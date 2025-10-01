# -----------------------------------------------------------------------------
# Makefile — Developer UX for DB, Docker and Runtime (LangGraph/Studio/API)
# -----------------------------------------------------------------------------
# Conventions:
# - `##` comments are displayed on `make help`.
# - Docker Compose controls Postgres services (`db`) and app (`app`).

# ----- Core tools & project metadata -----------------------------------------
SHELL          := /bin/bash
PROJECT        ?= $(notdir $(CURDIR))
DOCKER         ?= docker
COMPOSE        ?= docker compose
COMPOSE_FILE   ?= docker-compose.yml
PY             ?= python

# ----- Images, containers, ports ---------------------------------------------
APP_IMAGE      ?= apllos/app:latest
APP_CONTAINER  ?= apllos-app
APP_SERVICE    ?= app
DB_SERVICE     ?= db
DB_CONTAINER   ?= $(DB_SERVICE)
APP_PORT       ?= 2024
STUDIO_PORT    ?= 2025
POSTGRES_PORT  ?= 5432

# ----- Paths used by scripts --------------------------------------------------
ANALYTICS_DIR  ?= $(CURDIR)/data/raw/analytics
DOCS_DIR       ?= $(CURDIR)/data/docs

# ----- Environment injection --------------------------------------------------
ENV_FILE ?= .env
# Se .env existir, injeta automaticamente via --env-file
ENV_ARGS := $(shell [ -f $(ENV_FILE) ] && echo --env-file $(ENV_FILE))

# ----- DB credentials (container defaults) -----------------------------------
DB_USER     ?= app
DB_PASSWORD ?= app
DB_NAME     ?= app

# ----- Connection strings -----------------------------------------------------
# Para containers via compose (hostname = nome do serviço)
DSN_COMPOSE ?= postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@$(DB_SERVICE):$(POSTGRES_PORT)/$(DB_NAME)
# Para docker run (macOS/Windows) conectando no DB do host
DSN_HOST    ?= postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@host.docker.internal:$(POSTGRES_PORT)/$(DB_NAME)

# ----- Seed SQL files ---------------------------------------------------------
DB_SEED_SCHEMA := data/samples/schema.sql
DB_SEED_DATA   := data/samples/seed.sql

# =============================================================================
# Help
# =============================================================================
## Show this help
.PHONY: help
help:
	@printf "\nAvailable targets:\n\n"; \
	awk '\
	  BEGIN { FS=":.*" } \
	  /^## / { desc=substr($$0,4); next } \
	  /^[a-zA-Z0-9_.-]+:($$|[^=])/ && $$1 != ".PHONY" { \
	    if (desc) { printf "  \033[36m%-22s\033[0m %s\n", $$1, desc; desc=""; } \
	  }' $(MAKEFILE_LIST) | sort

# =============================================================================
# Directories
# =============================================================================
## Create local data directories expected by scripts
.PHONY: dirs
dirs:
	@mkdir -p data/raw/analytics data/docs data/samples

# =============================================================================
# Docker Compose wrappers (db + app)
# =============================================================================
## docker compose up -d (builds if needed)
.PHONY: compose-up
compose-up:
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) -f $(COMPOSE_FILE) up -d --build

## docker compose down (all services)
.PHONY: compose-down
compose-down:
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) -f $(COMPOSE_FILE) down

# =============================================================================
# Database lifecycle (service `db`)
# =============================================================================
## Start Postgres service via Docker Compose
.PHONY: db-start
db-start:
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) -f $(COMPOSE_FILE) up -d $(DB_SERVICE)

## Wait until Postgres is ready to accept connections
.PHONY: db-wait
db-wait:
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@echo "[db-wait] Waiting for database..."; \
	for i in $$(seq 1 30); do \
	  if $(COMPOSE) exec -T $(DB_SERVICE) sh -lc 'pg_isready -h 127.0.0.1 -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -t 1' >/dev/null 2>&1; then \
	    echo "[db-wait] Database is ready"; exit 0; \
	  fi; \
	  sleep 1; \
	done; \
	echo "[db-wait] Timeout waiting for DB"; exit 1

## Create extensions (vector, uuid-ossp) if present (idempotent)
.PHONY: db-init
db-init:
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) exec -T $(DB_SERVICE) sh -lc 'psql -v ON_ERROR_STOP=1 -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS vector;" || true'
	@$(COMPOSE) exec -T $(DB_SERVICE) sh -lc 'psql -v ON_ERROR_STOP=1 -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" || true'

## Tail Postgres logs
.PHONY: db-logs
db-logs:
	@$(COMPOSE) logs -f $(DB_SERVICE)

## Apply data/samples/schema.sql and data/samples/seed.sql
.PHONY: db-seed
db-seed:
	@test -f $(DB_SEED_SCHEMA) || { echo "\n[db-seed] Missing $(DB_SEED_SCHEMA)."; exit 1; }
	@echo "[db-seed] Applying schema: $(DB_SEED_SCHEMA)"
	@$(COMPOSE) exec -T $(DB_SERVICE) sh -lc 'psql -v ON_ERROR_STOP=1 -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -f -' < "$(DB_SEED_SCHEMA)"
	@if [ -f $(DB_SEED_DATA) ]; then \
	  echo "[db-seed] Applying seed data: $(DB_SEED_DATA)"; \
	  $(COMPOSE) exec -T $(DB_SERVICE) sh -lc 'psql -v ON_ERROR_STOP=1 -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -f -' < "$(DB_SEED_DATA)"; \
	else \
	  echo "[db-seed] No seed file found (skipping): $(DB_SEED_DATA)"; \
	fi

## Open interactive psql inside the db container
.PHONY: db-psql
db-psql:
	@$(COMPOSE) exec $(DB_SERVICE) psql -U $$POSTGRES_USER -d $$POSTGRES_DB

## Apply arbitrary SQL file: make db-sql FILE=path/to/file.sql
.PHONY: db-sql
db-sql:
	@test -n "$(FILE)" || { echo "Usage: make db-sql FILE=path/to/file.sql"; exit 2; }
	@test -f "$(FILE)" || { echo "File not found: $(FILE)"; exit 2; }
	@$(COMPOSE) exec -T $(DB_SERVICE) sh -lc 'psql -v ON_ERROR_STOP=1 -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -f -' < "$(FILE)"

## Stop Postgres service
.PHONY: db-stop
db-stop:
	@$(COMPOSE) stop $(DB_SERVICE) || true

## Stop and remove Postgres + volumes (DANGEROUS – wipes data)
.PHONY: db-reset
db-reset:
	@$(COMPOSE) down -v

# =============================================================================
# Application image lifecycle
# =============================================================================
DOCKERFILE ?= Dockerfile

## Build the application image
.PHONY: app-build
app-build:
	@test -f $(DOCKERFILE) || { echo "$(DOCKERFILE) not found"; exit 2; }
	@$(DOCKER) build -t $(APP_IMAGE) -f $(DOCKERFILE) .

## Run dev container mounting the repo (override CMD="...")
.PHONY: app-run
app-run: dirs
	@$(DOCKER) run --rm -it \
	  --name $(APP_CONTAINER) \
	  -p $(APP_PORT):$(APP_PORT) -p $(STUDIO_PORT):$(STUDIO_PORT) \
	  -v "$(CURDIR)":/workspace \
	  -v "$(ANALYTICS_DIR)":/workspace/data/raw/analytics \
	  -v "$(DOCS_DIR)":/workspace/data/docs \
	  $(ENV_ARGS) \
	  -w /workspace \
	  $(APP_IMAGE) $(CMD)

## Open an interactive shell in app container
.PHONY: app-sh
app-sh:
	@$(MAKE) app-run CMD=bash

# =============================================================================
# Data ingestion helpers (executed inside ephemeral app container)
# =============================================================================
## Load Olist CSVs into Postgres (scripts/ingest_analytics.py)
.PHONY: ingest-analytics
ingest-analytics:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  -v "$(ANALYTICS_DIR)":/workspace/data/raw/analytics \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/ingest_analytics.py

## Load Olist CSVs, truncating tables first (idempotent re-run)
.PHONY: ingest-analytics-truncate
ingest-analytics-truncate:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  -v "$(ANALYTICS_DIR)":/workspace/data/raw/analytics \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/ingest_analytics.py --truncate --analyze

## Chunk + embed docs into pgvector (scripts/ingest_vectors.py)
.PHONY: ingest-vectors
ingest-vectors:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  -v "$(DOCS_DIR)":/workspace/data/docs \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/ingest_vectors.py

## Explain/analyze SQL via scripts/explain_sql.py; pass SQL="..."
.PHONY: explain-sql
explain-sql:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/explain_sql.py "$(SQL)"

## Ingest CSVs with defaults (docker-run → host DB)
.PHONY: ingest-analytics-all
ingest-analytics-all:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  -v "$(ANALYTICS_DIR)":/workspace/data/raw/analytics \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/ingest_analytics.py \
	    --schema /workspace/data/samples/schema.sql \
	    --data-dir /workspace/data/raw/analytics

## Ingest docs into pgvector with defaults (docker-run → host DB)
.PHONY: ingest-vectors-all
ingest-vectors-all:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  -v "$(DOCS_DIR)":/workspace/data/docs \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/ingest_vectors.py \
	    --docs-dir /workspace/data/docs

## Generate analytics allowlist JSON from live DB schema
.PHONY: gen-allowlist
gen-allowlist:
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/gen_allowlist.py \
	    --out /workspace/app/routing/allowlist.json

# =============================================================================
# Runtime shortcuts: LangGraph Server (Studio) & API
# =============================================================================
# Observação: CLI atual usa `langgraph dev` e lê `langgraph.json` na raiz.
# Criamos esse arquivo automaticamente se não existir.
define LG_JSON
{
  "dependencies": ["./"],
  "graphs": { "assistant": "./app/graph/assistant.py:get_assistant" },
  "env": "./.env"
}
endef
export LG_JSON

## Run LangGraph (dev server) on :$(APP_PORT) (docker run)
.PHONY: studio-run
studio-run:
	@[ -s langgraph.json ] || printf '%s\n' '{' '  "dependencies": ["./"],' '  "graphs": { "assistant": "./app/graph/assistant.py:get_assistant" },' '  "env": "./.env"' '}' > langgraph.json
	@$(DOCKER) run --rm --name $(APP_CONTAINER)-studio \
	  -p $(APP_PORT):$(APP_PORT) \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -e REQUIRE_SQL_APPROVAL=false \
	  -w /workspace \
	  $(APP_IMAGE) langgraph dev --host 0.0.0.0 --port $(APP_PORT) --allow-blocking

## Run LangGraph (dev server) via docker compose run (service `app`)
.PHONY: studio-compose
studio-compose:
	@[ -s langgraph.json ] || printf '%s\n' '{' '  "dependencies": ["./"],' '  "graphs": { "assistant": "./app/graph/assistant.py:get_assistant" },' '  "env": "./.env"' '}' > langgraph.json
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) run --rm --service-ports \
	  -e DATABASE_URL="$(DSN_COMPOSE)" \
	  $(APP_SERVICE) \
	  langgraph dev --host 0.0.0.0 --port $(APP_PORT)

## Run FastAPI app on :8000 (docker run)
.PHONY: api-run
api-run:
	@$(DOCKER) run --rm --name $(APP_CONTAINER)-api \
	  -p 8000:8000 \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) uvicorn app.api.server:get_app --host 0.0.0.0 --port 8000

# =============================================================================
# One-shot flows
# =============================================================================
## Full setup: dirs + db + schema/seed + build + ingestions + allowlist
.PHONY: bootstrap
bootstrap: dirs db-start db-wait db-init db-seed app-build ingest-analytics-all ingest-vectors-all gen-allowlist
	@echo "Bootstrap completed."

## Bootstrap everything and start LangGraph Server
.PHONY: studio-up
studio-up: bootstrap
	@$(MAKE) studio-run

## Bootstrap everything and start FastAPI server
.PHONY: api-up
api-up: bootstrap
	@$(MAKE) api-run

# =============================================================================
# Query Interface
# =============================================================================
## Query the assistant: make query QUERY="sua pergunta" [ATTACHMENT="caminho/do/arquivo"]
.PHONY: query
query:
	@if [ -z "$(QUERY)" ] && [ -z "$(ATTACHMENT)" ]; then \
		echo "Usage: make query QUERY=\"sua pergunta\" [ATTACHMENT=\"caminho/do/arquivo\"]"; \
		echo "Examples:"; \
		echo "  make query QUERY=\"Como iniciar um e-commerce?\""; \
		echo "  make query QUERY=\"Quantos pedidos temos?\" ATTACHMENT=\"data/samples/invoice.pdf\""; \
		echo "  make query ATTACHMENT=\"data/samples/order.txt\""; \
		exit 1; \
	fi
	@$(DOCKER) run --rm \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  --network host \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) scripts/query_assistant.py \
	    --query "$(QUERY)" \
	    --attachment "$(ATTACHMENT)" \
	    --base-url "http://localhost:2024"

# =============================================================================
# Housekeeping
# =============================================================================
## Remove dangling containers/images/networks/volumes (CAUTION)
.PHONY: prune
prune:
	@$(DOCKER) system prune -f --volumes

## Remove Python caches and build artifacts
.PHONY: clean
clean:
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@rm -rf .pytest_cache .mypy_cache dist build *.egg-info