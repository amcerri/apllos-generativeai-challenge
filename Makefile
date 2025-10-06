# -----------------------------------------------------------------------------
# Makefile — Developer UX for DB, Docker and Runtime (LangGraph/Studio/API)
# -----------------------------------------------------------------------------
# Conventions:
# - `##` comments are displayed on `make help`.
# - Docker Compose controls Postgres services (`db`) and app (`app`).

# ----- Core tools & project metadata -----------------------------------------
SHELL          := /bin/bash
PROJECT        ?= apllos-generativeai-challenge
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
# If .env exists, inject automatically via --env-file
ENV_ARGS := $(shell [ -f $(ENV_FILE) ] && echo --env-file $(ENV_FILE))

# ----- DB credentials (container defaults) -----------------------------------
DB_USER     ?= app
DB_PASSWORD ?= app
DB_NAME     ?= app

# ----- Connection strings -----------------------------------------------------
# For containers via compose (hostname = service name)
DSN_COMPOSE ?= postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@$(DB_SERVICE):$(POSTGRES_PORT)/$(DB_NAME)
# For docker run (macOS/Windows) connecting to host DB
DSN_HOST    ?= postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@host.docker.internal:$(POSTGRES_PORT)/$(DB_NAME)

# ----- Seed SQL files ---------------------------------------------------------
DB_SEED_SCHEMA := data/samples/schema.sql
DB_SEED_DATA   := data/samples/seed.sql

# =============================================================================
# Help & Documentation
# =============================================================================

.PHONY: help
help: ## Show this help message
	@echo "Apllos Assistant - Development Commands"
	@echo "======================================"
	@echo ""
	@echo "BOOTSTRAP & RESET:"
	@echo "  bootstrap          - Complete bootstrap: reset + minimal setup + start + ingest real data + test"
	@echo "  bootstrap-complete - GUARANTEED complete bootstrap with step-by-step data loading"
	@echo "  reset              - Complete reset: stop all + remove containers + clean volumes (keeps data)"
	@echo ""
	@echo "DIRECTORY MANAGEMENT:"
	@echo "  dirs          - Create required directories"
	@echo ""
	@echo "DOCKER MANAGEMENT:"
	@echo "  docker-build  - Build application Docker image"
	@echo "  docker-stop   - Stop all containers"
	@echo "  docker-remove - Remove all containers"
	@echo "  docker-clean  - Remove containers + images + volumes"
	@echo "  docker-reset  - Complete Docker reset (stop + remove + clean)"
	@echo ""
	@echo "DATABASE MANAGEMENT:"
	@echo "  db-start      - Start PostgreSQL container"
	@echo "  db-stop       - Stop PostgreSQL container"
	@echo "  db-wait       - Wait for database to be ready"
	@echo "  db-init       - Initialize database (extensions, roles)"
	@echo "  db-seed       - Seed database with sample data"
	@echo "  db-reset      - Reset database (drop + recreate + init + seed)"
	@echo "  db-psql       - Connect to database via psql"
	@echo "  db-status     - Show database status"
	@echo ""
	@echo "DATA INGESTION:"
	@echo "  ingest-analytics - Ingest analytics data from CSVs"
	@echo "  ingest-vectors   - Ingest document vectors for RAG"
	@echo "  gen-allowlist    - Generate allowlist from database schema"
	@echo "  ingest-all       - Run all ingestion processes"
	@echo ""
	@echo "APPLICATION RUNTIME:"
	@echo "  studio-up     - Start LangGraph Studio (recommended for development)"
	@echo "  studio-down   - Stop LangGraph Studio"
	@echo "  api-up        - Start FastAPI server"
	@echo "  api-down      - Stop FastAPI server"
	@echo "  app-status    - Show application status"
	@echo ""
	@echo "TESTING & VALIDATION:"
	@echo "  test          - Run all tests"
	@echo "  test-unit     - Run unit tests"
	@echo "  test-e2e      - Run end-to-end tests"
	@echo "  validate      - Validate system health"
	@echo "  query         - Test query (usage: make query QUERY=\"your question\" [ATTACHMENT=\"path/to/file\"])"
	@echo "                  Examples:"
	@echo "                    make query QUERY=\"quantos pedidos temos?\""
	@echo "                    make query ATTACHMENT=\"data/samples/order.txt\""
	@echo "                    make query QUERY=\"analise este pedido\" ATTACHMENT=\"data/samples/order.txt\""
	@echo "  batch-query   - Process multiple queries from YAML file (INPUT='queries.yaml' [OUTPUT='results.md'])"
	@echo ""
	@echo "UTILITIES:"
	@echo "  install-deps  - Install/update Python dependencies from pyproject.toml"
	@echo "  logs          - Show application logs"
	@echo "  logs-db       - Show database logs"
	@echo "  shell         - Open shell in application container"
	@echo "  shell-db      - Open shell in database container"
	@echo "  clean         - Clean temporary files and caches"
	@echo "  clean-data    - Remove data directories (WARNING: deletes CSVs and PDFs)"

# =============================================================================
# Bootstrap & Reset (Main Commands)
# =============================================================================

.PHONY: bootstrap
bootstrap: ## Complete bootstrap: reset + setup + start + ingest + test
	@echo "Starting complete bootstrap..."
	@echo "============================="
	@$(MAKE) reset
	@$(MAKE) setup-minimal
	@$(MAKE) docker-build
	@echo "Waiting for database to be ready for ingestion..."
	@$(MAKE) db-wait
	@$(MAKE) ingest-all
	@$(MAKE) studio-up
	@$(MAKE) validate
	@echo "Bootstrap complete! System is ready."

.PHONY: bootstrap-complete
bootstrap-complete: ## Complete bootstrap with guaranteed data loading
	@echo "Starting COMPLETE bootstrap with data loading..."
	@echo "==============================================="
	@echo "Step 1: Complete reset..."
	@$(MAKE) reset
	@echo "Step 2: Setup database and directories..."
	@$(MAKE) setup-minimal
	@echo "Step 3: Build Docker image..."
	@$(MAKE) docker-build
	@echo "Step 4: Wait for database to be fully ready..."
	@sleep 5
	@$(MAKE) db-wait
	@echo "Step 5: Load real analytics data..."
	@$(MAKE) ingest-analytics
	@echo "Step 6: Load document vectors..."
	@$(MAKE) ingest-vectors
	@echo "Step 7: Generate allowlist..."
	@$(MAKE) gen-allowlist
	@echo "Step 8: Start LangGraph Studio..."
	@$(MAKE) studio-up
	@echo "Step 9: Validate system..."
	@$(MAKE) validate
	@echo "COMPLETE BOOTSTRAP FINISHED! System ready with real data."

.PHONY: reset
reset: ## Complete reset: stop all + remove containers + clean volumes
	@echo "Starting complete reset..."
	@echo "=========================="
	@$(MAKE) docker-reset
	@echo "Complete reset finished."

.PHONY: setup
setup: ## Setup environment: create dirs + start db + init + seed
	@echo "Setting up environment..."
	@echo "========================="
	@$(MAKE) dirs
	@$(MAKE) db-start
	@$(MAKE) db-wait
	@$(MAKE) db-init
	@$(MAKE) db-seed
	@echo "Setup complete."

.PHONY: setup-minimal
setup-minimal: ## Setup environment without sample data: create dirs + start db + init only
	@echo "Setting up minimal environment..."
	@echo "================================="
	@$(MAKE) dirs
	@$(MAKE) db-start
	@$(MAKE) db-wait
	@$(MAKE) db-init
	@echo "Minimal setup complete (no sample data)."

.PHONY: start
start: ## Start application: build + start studio
	@echo "Starting application..."
	@echo "======================="
	@$(MAKE) docker-build
	@$(MAKE) studio-up
	@echo "Application started."

# =============================================================================
# Directory Management
# =============================================================================

.PHONY: dirs
dirs: ## Create required directories
	@echo "Creating directories..."
	@mkdir -p "$(ANALYTICS_DIR)"
	@mkdir -p "$(DOCS_DIR)"
	@echo "Directories created."

.PHONY: clean-data
clean-data: ## Remove data directories (WARNING: deletes CSVs and PDFs)
	@echo "WARNING: This will delete all data files (CSVs, PDFs)!"
	@echo "Press Ctrl+C to cancel, or Enter to continue..."
	@read dummy
	@echo "Cleaning data directories..."
	@rm -rf "$(ANALYTICS_DIR)"
	@rm -rf "$(DOCS_DIR)"
	@echo "Data directories cleaned."

# =============================================================================
# Docker Management
# =============================================================================

.PHONY: docker-build
docker-build: ## Build application Docker image
	@echo "Building Docker image..."
	@$(DOCKER) build -t $(APP_IMAGE) .
	@echo "Docker image built."

.PHONY: docker-stop
docker-stop: ## Stop all containers
	@echo "Stopping containers..."
	@$(COMPOSE) down 2>/dev/null || true
	@$(DOCKER) stop $(APP_CONTAINER)-studio 2>/dev/null || true
	@$(DOCKER) stop $(APP_CONTAINER)-api 2>/dev/null || true
	@echo "Containers stopped."

.PHONY: docker-remove
docker-remove: ## Remove all containers
	@echo "Removing containers..."
	@$(COMPOSE) down --remove-orphans 2>/dev/null || true
	@$(DOCKER) rm $(APP_CONTAINER)-studio 2>/dev/null || true
	@$(DOCKER) rm $(APP_CONTAINER)-api 2>/dev/null || true
	@echo "Containers removed."

.PHONY: docker-clean
docker-clean: ## Remove containers + images + volumes
	@echo "Cleaning Docker resources..."
	@$(MAKE) docker-remove
	@echo "Removing images..."
	@$(DOCKER) rmi $(APP_IMAGE) 2>/dev/null || true
	@$(DOCKER) image prune -f
	@echo "Removing volumes..."
	@$(DOCKER) volume rm $(PROJECT)_pgdata 2>/dev/null || true
	@$(DOCKER) volume rm $(PROJECT)_postgres_data 2>/dev/null || true
	@$(DOCKER) volume prune -f
	@echo "Docker resources cleaned."

.PHONY: docker-reset
docker-reset: ## Complete Docker reset (stop + remove + clean)
	@echo "Resetting Docker..."
	@echo "=================="
	@$(MAKE) docker-stop
	@$(MAKE) docker-remove
	@$(MAKE) docker-clean
	@echo "Docker reset complete."

# =============================================================================
# Database Management
# =============================================================================

.PHONY: db-start
db-start: ## Start PostgreSQL container
	@echo "Starting database..."
	@$(COMPOSE) up -d $(DB_SERVICE)
	@echo "Database started."

.PHONY: db-stop
db-stop: ## Stop PostgreSQL container
	@echo "Stopping database..."
	@$(COMPOSE) stop $(DB_SERVICE)
	@echo "Database stopped."

.PHONY: db-wait
db-wait: ## Wait for database to be ready
	@echo "Waiting for database..."
	@for i in $$(seq 1 60); do \
		if $(COMPOSE) exec $(DB_SERVICE) pg_isready -U $(DB_USER) >/dev/null 2>&1; then \
			echo "Database is ready."; \
			exit 0; \
		fi; \
		echo "Waiting... ($$i/60)"; \
	  sleep 1; \
	done; \
	echo "Database not ready after 60 seconds"; \
	exit 1

.PHONY: db-init
db-init: ## Initialize database (extensions, roles)
	@echo "Initializing database..."
	@$(COMPOSE) exec $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME) -c "CREATE EXTENSION IF NOT EXISTS vector;"
	@$(COMPOSE) exec $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME) -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;"
	@echo "Database initialized."

.PHONY: db-seed
db-seed: ## Seed database with sample data
	@echo "Seeding database..."
	@if [ -f $(DB_SEED_SCHEMA) ]; then \
		$(COMPOSE) exec -T $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME) < $(DB_SEED_SCHEMA); \
	fi
	@if [ -f $(DB_SEED_DATA) ]; then \
		$(COMPOSE) exec -T $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME) < $(DB_SEED_DATA); \
	fi
	@echo "Database seeded."

.PHONY: db-reset
db-reset: ## Reset database (drop + recreate + init + seed)
	@echo "Resetting database..."
	@echo "===================="
	@$(MAKE) db-stop
	@$(DOCKER) volume rm $(PROJECT)_postgres_data 2>/dev/null || true
	@$(MAKE) db-start
	@$(MAKE) db-wait
	@$(MAKE) db-init
	@$(MAKE) db-seed
	@echo "Database reset complete."

.PHONY: db-psql
db-psql: ## Connect to database via psql
	@echo "Connecting to database..."
	@$(COMPOSE) exec $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME)

.PHONY: db-status
db-status: ## Show database status
	@echo "Database Status:"
	@echo "================"
	@$(COMPOSE) ps $(DB_SERVICE)
	@echo ""
	@echo "Database Info:"
	@$(COMPOSE) exec $(DB_SERVICE) psql -U $(DB_USER) -d $(DB_NAME) -c "SELECT version();" 2>/dev/null || echo "Database not accessible"

# =============================================================================
# Data Ingestion
# =============================================================================

.PHONY: ingest-analytics
ingest-analytics: ## Ingest analytics data from CSVs
	@echo "Ingesting analytics data..."
	@DATABASE_URL="postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@localhost:$(POSTGRES_PORT)/$(DB_NAME)" $(PY) scripts/ingest_analytics.py \
		--schema "$(DB_SEED_SCHEMA)" \
		--data-dir "$(ANALYTICS_DIR)" \
		--truncate --analyze
	@echo "Analytics data ingested."

.PHONY: ingest-vectors
ingest-vectors: ## Ingest document vectors for RAG
	@echo "Ingesting document vectors..."
	@DATABASE_URL="postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@localhost:$(POSTGRES_PORT)/$(DB_NAME)" $(PY) scripts/ingest_vectors.py \
		--docs-dir "$(DOCS_DIR)" \
		--model $(shell $(PY) -c "import yaml; print(yaml.safe_load(open('app/config/models.yaml'))['models']['embeddings']['name'])")
	@echo "Document vectors ingested."

.PHONY: gen-allowlist
gen-allowlist: ## Generate allowlist from database schema
	@echo "Generating allowlist..."
	@DATABASE_URL="postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@localhost:$(POSTGRES_PORT)/$(DB_NAME)" $(PY) scripts/gen_allowlist.py \
		--schema "$(DB_SEED_SCHEMA)" \
		--out app/routing/allowlist.json
	@echo "Allowlist generated."

.PHONY: ingest-all
ingest-all: ## Run all ingestion processes
	@echo "Running all ingestion processes..."
	@echo "================================="
	@$(MAKE) ingest-analytics
	@$(MAKE) ingest-vectors
	@$(MAKE) gen-allowlist
	@echo "All ingestion processes complete."

# =============================================================================
# Application Runtime
# =============================================================================

.PHONY: studio-up
studio-up: ## Start LangGraph Studio (recommended for development)
	@echo "Starting LangGraph Studio..."
	@$(MAKE) docker-build
	@$(DOCKER) run --rm --name $(APP_CONTAINER)-studio \
	  -p $(APP_PORT):$(APP_PORT) \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e BG_JOB_ISOLATED_LOOPS=true \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -e REQUIRE_SQL_APPROVAL=false \
	  -w /workspace \
	  $(APP_IMAGE) langgraph dev --host 0.0.0.0 --port $(APP_PORT)
	@echo "LangGraph Studio started."

.PHONY: studio-down
studio-down: ## Stop LangGraph Studio
	@echo "Stopping LangGraph Studio..."
	@$(DOCKER) stop $(APP_CONTAINER)-studio 2>/dev/null || true
	@$(DOCKER) rm $(APP_CONTAINER)-studio 2>/dev/null || true
	@echo "LangGraph Studio stopped."

.PHONY: api-up
api-up: ## Start FastAPI server
	@echo "Starting FastAPI server..."
	@$(MAKE) docker-build
	@$(DOCKER) run --rm --name $(APP_CONTAINER)-api \
	  -p 8000:8000 \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
	  $(APP_IMAGE) uvicorn app.api.server:get_app --host 0.0.0.0 --port 8000
	@echo "FastAPI server started."

.PHONY: api-down
api-down: ## Stop FastAPI server
	@echo "Stopping FastAPI server..."
	@$(DOCKER) stop $(APP_CONTAINER)-api 2>/dev/null || true
	@$(DOCKER) rm $(APP_CONTAINER)-api 2>/dev/null || true
	@echo "FastAPI server stopped."

.PHONY: app-status
app-status: ## Show application status
	@echo "Application Status:"
	@echo "==================="
	@echo "Studio Container:"
	@$(DOCKER) ps --filter name=$(APP_CONTAINER)-studio --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Not running"
	@echo ""
	@echo "API Container:"
	@$(DOCKER) ps --filter name=$(APP_CONTAINER)-api --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Not running"
	@echo ""
	@echo "Studio URL: https://smith.langchain.com/studio/?baseUrl=http://localhost:$(APP_PORT)"
	@echo "API URL: http://localhost:8000/docs"

# =============================================================================
# Testing & Validation
# =============================================================================

.PHONY: test
test: ## Run all tests
	@echo "Running all tests..."
	@$(PY) -m pytest tests/ -v
	@echo "All tests completed."

.PHONY: test-unit
test-unit: ## Run unit tests
	@echo "Running unit tests..."
	@$(PY) -m pytest tests/unit/ -v
	@echo "Unit tests completed."

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	@echo "Running end-to-end tests..."
	@$(PY) -m pytest tests/e2e/ -v
	@echo "End-to-end tests completed."

.PHONY: validate
validate: ## Validate system health
	@echo "Validating system health..."
	@echo "Checking Docker containers..."
	@docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E '(apllos|postgres)' || echo "No containers running"
	@echo "Checking database connection..."
	@docker exec apllos-generativeai-challenge-postgres psql -U app -d app -c 'SELECT 1;' >/dev/null 2>&1 && echo "Database OK" || echo "Database not accessible"
	@echo "Testing query functionality..."
	@$(MAKE) query QUERY="system health check" >/dev/null 2>&1 && echo "Query system OK" || echo "Query system not responding"
	@echo "System validation completed."

.PHONY: query
query: ## Test query (usage: make query QUERY="your question" [ATTACHMENT="path/to/file"] [THREAD_ID="thread_id"])
	@if [ -z "$(QUERY)" ] && [ -z "$(ATTACHMENT)" ]; then \
		echo "Please provide a query or attachment: make query QUERY=\"your question\" [ATTACHMENT=\"path/to/file\"] [THREAD_ID=\"thread_id\"]"; \
		exit 1; \
	fi
	@if [ -n "$(QUERY)" ] && [ -n "$(ATTACHMENT)" ] && [ -n "$(THREAD_ID)" ]; then \
		echo "Testing query with attachment: $(QUERY) + $(ATTACHMENT) (Thread: $(THREAD_ID))"; \
		$(PY) scripts/query_assistant.py --query "$(QUERY)" --attachment "$(ATTACHMENT)" --thread-id "$(THREAD_ID)"; \
	elif [ -n "$(QUERY)" ] && [ -n "$(ATTACHMENT)" ]; then \
		echo "Testing query with attachment: $(QUERY) + $(ATTACHMENT)"; \
		$(PY) scripts/query_assistant.py --query "$(QUERY)" --attachment "$(ATTACHMENT)"; \
	elif [ -n "$(QUERY)" ] && [ -n "$(THREAD_ID)" ]; then \
		echo "Testing query: $(QUERY) (Thread: $(THREAD_ID))"; \
		$(PY) scripts/query_assistant.py --query "$(QUERY)" --thread-id "$(THREAD_ID)"; \
	elif [ -n "$(QUERY)" ]; then \
		echo "Testing query: $(QUERY)"; \
		$(PY) scripts/query_assistant.py --query "$(QUERY)"; \
	else \
		echo "Testing attachment: $(ATTACHMENT)"; \
		$(PY) scripts/query_assistant.py --attachment "$(ATTACHMENT)"; \
	fi

.PHONY: batch-query
batch-query: ## Process multiple queries from YAML file (INPUT="queries.yaml" [OUTPUT="results.md"])
	@if [ -z "$(INPUT)" ]; then echo "Error: INPUT parameter required. Usage: make batch-query INPUT=queries.yaml [OUTPUT=results.md]"; exit 1; fi
	@echo "Processing batch queries from $(INPUT)..."
	@$(PY) scripts/batch_query.py --input "$(INPUT)" $(if $(OUTPUT),--output "$(OUTPUT)")

.PHONY: test-commerce
test-commerce: ## Test Commerce Agent with batch queries (INPUT="test_commerce.yaml" [OUTPUT="commerce_test.md"])
	@if [ -z "$(INPUT)" ]; then echo "Error: INPUT parameter required. Usage: make test-commerce INPUT=test_commerce.yaml [OUTPUT=commerce_test.md]"; exit 1; fi
	@echo "Testing Commerce Agent with $(INPUT)..."
	@$(PY) scripts/test_commerce_batch.py --input "$(INPUT)" $(if $(OUTPUT),--output "$(OUTPUT)")

.PHONY: logs
logs: ## Show real-time logs from LangGraph Studio container
	@if docker ps --format '{{.Names}}' | grep -q "apllos-app-studio"; then \
		echo "Showing real-time logs from LangGraph Studio..."; \
		echo "Press Ctrl+C to stop following logs"; \
		docker logs -f apllos-app-studio; \
	else \
		echo "LangGraph Studio container not running."; \
		echo "Start it with: make studio-up"; \
		echo ""; \
		echo "Available containers:"; \
		docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" || echo "No containers running"; \
	fi

# =============================================================================
# Utilities
# =============================================================================


.PHONY: logs-db
logs-db: ## Show database logs
	@echo "Database logs:"
	@$(COMPOSE) logs $(DB_SERVICE) --tail 50

.PHONY: shell
shell: ## Open shell in application container
	@echo "Opening shell in application container..."
	@$(DOCKER) run --rm -it \
	  -v "$(CURDIR)":/workspace \
	  $(ENV_ARGS) \
	  -e DATABASE_URL="$(DSN_HOST)" \
	  -w /workspace \
		$(APP_IMAGE) /bin/bash

.PHONY: shell-db
shell-db: ## Open shell in database container
	@echo "Opening shell in database container..."
	@$(COMPOSE) exec $(DB_SERVICE) /bin/bash

.PHONY: clean
clean: ## Clean temporary files and caches
	@echo "Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.log" -delete
	@find . -type d -name ".pytest_cache" -delete
	@find . -type d -name ".mypy_cache" -delete
	@echo "Cleanup completed."

.PHONY: install-deps
install-deps: ## Install/update Python dependencies from pyproject.toml
	@echo "Installing Python dependencies..."
	@$(PY) -m pip install --upgrade pip
	@$(PY) -m pip install -e .
	@echo "Dependencies installed."

# =============================================================================
# Default target
# =============================================================================

.DEFAULT_GOAL := help