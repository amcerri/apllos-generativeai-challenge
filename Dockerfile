# -----------------------------------------------------------------------------
# Dockerfile — App image with LangGraph CLI
# -----------------------------------------------------------------------------
FROM python:3.11-slim

# Python runtime defaults: no .pyc, unbuffered logs, no pip cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps (psycopg binary roda sem headers, mas libpq5 é útil)
RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential gcc libpq5 curl git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

 # App user
RUN groupadd -g 1000 app || true && useradd -m -u 1000 -g 1000 -s /bin/bash app
WORKDIR /workspace

 # Python deps
COPY --chown=app:app pyproject.toml README.md ./
RUN set -eux; \
    python -m pip install --upgrade pip wheel; \
    # CLI atual do LangGraph (com backend in-memory para dev)
    pip install --no-cache-dir "langgraph-cli[inmem]" ; \
    # instala o projeto (usa pyproject)
    pip install --no-cache-dir .

 # App code and runtime assets
COPY --chown=app:app app ./app
COPY --chown=app:app scripts ./scripts
COPY --chown=app:app app/config ./app/config
COPY --chown=app:app app/prompts ./app/prompts
# samples (schema/seed) se existirem
COPY --chown=app:app data/samples ./data/samples

# Non-root
USER app

EXPOSE 2024 2025 8000

# Default command: shell (Makefile/compose substituem quando necessário)
CMD ["bash"]