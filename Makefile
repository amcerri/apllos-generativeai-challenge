# Makefile — Docker-first developer experience for apllos-generativeai-challenge
# Usage: `make help` to list all targets.

SHELL := bash
.DEFAULT_GOAL := help

# -----------------------------------------------------------------------------
# Project settings
# -----------------------------------------------------------------------------
PROJECT_NAME       ?= apllos-generativeai-challenge
NETWORK            ?= $(PROJECT_NAME)-net
ENV_FILE           ?= .env
ENV_ARGS          := $(if $(wildcard $(ENV_FILE)),--env-file $(ENV_FILE),)

# -----------------------------------------------------------------------------
# Images & containers
# -----------------------------------------------------------------------------
# Database (Postgres + pgvector)
DB_IMAGE           ?= pgvector/pgvector:pg16
DB_CONTAINER       ?= $(PROJECT_NAME)-postgres
DB_VOLUME          ?= $(PROJECT_NAME)-pgdata
DB_PORT            ?= 5432
DB_USER            ?= app
DB_PASSWORD        ?= app
DB_NAME            ?= app

# Application image (built from Dockerfile when available)
APP_IMAGE          ?= $(PROJECT_NAME)-app:dev
APP_CONTAINER      ?= $(PROJECT_NAME)-app
APP_PORT           ?= 2024
STUDIO_PORT        ?= 2025

# Host paths to mount into containers (created lazily)
DATA_DIR           ?= $(CURDIR)/data
ANALYTICS_DIR      ?= $(DATA_DIR)/raw/analytics
DOCS_DIR           ?= $(DATA_DIR)/docs
BACKUPS_DIR        ?= $(CURDIR)/backups

DOCKER             ?= docker
COMPOSE            ?= docker compose

# Colors for pretty help
CYAN  := \033[36m
GREEN := \033[32m
RESET := \033[0m

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
.PHONY: help
help: ## Show this help
	@echo -e "$(CYAN)Available targets$(RESET)"
	@awk 'BEGIN {FS = ":.*##"}; /^[a-zA-Z0-9_.-]+:.*##/ {printf "  $(GREEN)%-26s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.PHONY: dirs
dirs: ## Create local data/ and backups/ folders if missing
	@mkdir -p "$(ANALYTICS_DIR)" "$(DOCS_DIR)" "$(BACKUPS_DIR)"

.PHONY: docker-info
docker-info: ## Show Docker and Compose versions
	@$(DOCKER) version
	@$(COMPOSE) version

.PHONY: network
network: ## Create the shared Docker network if absent
	@$(DOCKER) network inspect $(NETWORK) >/dev/null 2>&1 || $(DOCKER) network create $(NETWORK)
	@echo "Network: $(NETWORK)"

# -----------------------------------------------------------------------------
# Database lifecycle (Postgres + pgvector)
# -----------------------------------------------------------------------------
.PHONY: db-start
db-start: dirs network ## Start Postgres (pgvector) container in background
	@$(DOCKER) volume inspect $(DB_VOLUME) >/dev/null 2>&1 || $(DOCKER) volume create $(DB_VOLUME) >/dev/null
	@$(DOCKER) run -d --name $(DB_CONTAINER) \
	  --restart unless-stopped \
	  --network $(NETWORK) \
	  -p $(DB_PORT):5432 \
	  -v $(DB_VOLUME):/var/lib/postgresql/data \
	  $(ENV_ARGS) \
	  -e POSTGRES_USER=$(DB_USER) \
	  -e POSTGRES_PASSWORD=$(DB_PASSWORD) \
	  -e POSTGRES_DB=$(DB_NAME) \
	  $(DB_IMAGE)
	@echo "Postgres is starting on localhost:$(DB_PORT) — container $(DB_CONTAINER)"

.PHONY: db-wait
db-wait: ## Wait until Postgres is ready to accept connections
	@echo "Waiting for Postgres to become ready..."
	@until $(DOCKER) exec $(DB_CONTAINER) pg_isready -h 127.0.0.1 -p 5432 -U $(DB_USER) >/dev/null 2>&1; do \
	  sleep 1; \
	  printf "."; \
	 done; echo " ready";

.PHONY: db-init
db-init: ## Initialize database extensions (vector)
	@$(DOCKER) exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -v ON_ERROR_STOP=1 -c "CREATE EXTENSION IF NOT EXISTS vector;"

.PHONY: db-logs
db-logs: ## Tail Postgres logs
	@$(DOCKER) logs -f --since=1m $(DB_CONTAINER)

.PHONY: db-psql
db-psql: ## Open psql shell inside the DB container
	@$(DOCKER) exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

.PHONY: db-sh
db-sh: ## Open a bash shell in the DB container
	@$(DOCKER) exec -it $(DB_CONTAINER) bash

.PHONY: db-stop
db-stop: ## Stop Postgres container
	@-$(DOCKER) stop $(DB_CONTAINER)

.PHONY: db-rm
db-rm: ## Remove Postgres container (keeps volume)
	@-$(DOCKER) rm -f $(DB_CONTAINER)

.PHONY: db-reset
db-reset: db-stop db-rm ## Remove container and volume (DANGEROUS)
	@-$(DOCKER) volume rm $(DB_VOLUME) || true

DATE := $(shell date +%Y%m%d-%H%M%S)

.PHONY: db-backup
db-backup: dirs ## Backup DB to ./backups/<dbname>-<timestamp>.sql
	@mkdir -p $(BACKUPS_DIR)
	@$(DOCKER) exec $(DB_CONTAINER) pg_dump -U $(DB_USER) -d $(DB_NAME) -F p > "$(BACKUPS_DIR)/$(DB_NAME)-$(DATE).sql"
	@echo "Backup written to $(BACKUPS_DIR)/$(DB_NAME)-$(DATE).sql"

.PHONY: db-restore
# Usage: make db-restore FILE=backups/app-20250101-101010.sql
FILE ?=

db-restore: ## Restore DB from a SQL dump (use FILE=...)
	@if [ -z "$(FILE)" ]; then echo "Provide FILE=<path-to-sql>"; exit 2; fi
	@cat "$(FILE)" | $(DOCKER) exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -v ON_ERROR_STOP=1

# -----------------------------------------------------------------------------
# Application image lifecycle (optional until Dockerfile exists)
# -----------------------------------------------------------------------------
DOCKERFILE ?= Dockerfile

.PHONY: app-build
app-build: ## Build the application image (requires Dockerfile)
	@if [ ! -f $(DOCKERFILE) ]; then echo "$(DOCKERFILE) not found — skipping"; exit 2; fi
	@$(DOCKER) build -t $(APP_IMAGE) -f $(DOCKERFILE) .

.PHONY: app-run
# Run the app container mounting the current repo for live editing.
# Customize CMD via CMD="python -m app.graph.assistant" or similar.
CMD ?= bash
app-run: dirs network ## Run the app container (dev) with repo mounted and custom CMD
	@$(DOCKER) run --rm -it \
	  --name $(APP_CONTAINER) \
	  --network $(NETWORK) \
	  -p $(APP_PORT):$(APP_PORT) -p $(STUDIO_PORT):$(STUDIO_PORT) \
	  -v "$(CURDIR)":/workspace \
	  -v "$(ANALYTICS_DIR)":/workspace/data/raw/analytics \
	  -v "$(DOCS_DIR)":/workspace/data/docs \
	  $(ENV_ARGS) \
	  -w /workspace \
	  $(APP_IMAGE) $(CMD)

.PHONY: app-sh
app-sh: ## Open an interactive shell in a new app container
	@$(MAKE) app-run CMD=bash

# -----------------------------------------------------------------------------
# Data ingestion & utilities (executed inside ephemeral app container)
# These targets expect scripts to exist later in the project. They will fail
# fast with a helpful message if not present yet.
# -----------------------------------------------------------------------------
PY ?= python

define RUN_APP_PY
	@if [ ! -f "$1" ]; then echo "Missing $1 (will exist in later phases)."; exit 2; fi; \
	$(DOCKER) run --rm \
	  --network $(NETWORK) \
	  -v "$(CURDIR)":/workspace \
	  -v "$(ANALYTICS_DIR)":/workspace/data/raw/analytics \
	  -v "$(DOCS_DIR)":/workspace/data/docs \
	  $(ENV_ARGS) \
	  -w /workspace \
	  $(APP_IMAGE) $(PY) $1 $(2)
endef

.PHONY: ingest-analytics
ingest-analytics: ## Load Olist CSVs into Postgres (scripts/ingest_analytics.py)
	@$(call RUN_APP_PY,scripts/ingest_analytics.py)

.PHONY: ingest-vectors
ingest-vectors: ## Chunk + embed docs into pgvector (scripts/ingest_vectors.py)
	@$(call RUN_APP_PY,scripts/ingest_vectors.py)

.PHONY: explain-sql
explain-sql: ## Run explain_sql.py utility (scripts/explain_sql.py SQL="...")
	@$(call RUN_APP_PY,scripts/explain_sql.py,"$(SQL)")

# -----------------------------------------------------------------------------
# Compose wrappers (only if docker-compose.yml exists)
# -----------------------------------------------------------------------------
COMPOSE_FILE ?= docker-compose.yml

.PHONY: compose-up
compose-up: ## docker compose up -d (if compose file exists)
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) -f $(COMPOSE_FILE) up -d

.PHONY: compose-down
compose-down: ## docker compose down (if compose file exists)
	@if [ ! -f $(COMPOSE_FILE) ]; then echo "$(COMPOSE_FILE) not found"; exit 2; fi
	@$(COMPOSE) -f $(COMPOSE_FILE) down

# -----------------------------------------------------------------------------
# Housekeeping
# -----------------------------------------------------------------------------
.PHONY: prune
prune: ## Remove dangling containers/images/networks/volumes (CAUTION)
	@$(DOCKER) system prune -f --volumes

.PHONY: clean
clean: ## Remove Python caches and build artifacts
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@rm -rf .pytest_cache .mypy_cache dist build *.egg-info
