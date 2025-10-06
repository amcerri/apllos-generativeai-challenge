## Levantamento de melhorias: adoção de nativos/stdlib em vez de customizações

### Objetivo
Documentar oportunidades para simplificar o projeto adotando recursos nativos do Python e padrões amplamente suportados, reduzindo dependências, código custom e complexidade operacional.

### Prioridades (alto impacto, baixo risco)
- **Logging**: simplificar stack e padronizar com `logging` da stdlib
- **Config**: consolidar em `Settings` (Pydantic) e aposentar loaders antigos
- **Validation**: mover validações para Pydantic, reduzir helpers custom
- **DB engine**: remover global mutável, padronizar factory/lifecycle

---

### 1) Logging: substituir structlog por stdlib pura
- **Estado atual**:
  - `app/infra/logging.py` usa `structlog` com integração ao `logging`.
- **Problema**:
  - Dependência e processadores custom aumentam complexidade; wrappers (`get_logger`) e formatação duplicada.
- **Proposta**:
  - Usar apenas `logging` + `LoggerAdapter`/`LogRecordFactory` com `contextvars` para contexto (component, trace_id, thread_id).
  - JSON opcional via `Formatter` custom simples ou `logging.config.dictConfig` controlado por `observability.yaml`.
- **Benefícios**: menos dependências, inicialização simples, interoperabilidade padrão.
- **Riscos**: perda de alguns processors do structlog; mitigável com `LogRecordFactory`.
- **Esforço**: médio (1–2h).
- **Passos sugeridos**:
  - Criar `configure_logging(settings)` stdlib-only (ex.: `app/infra/logging_std.py`).
  - Manter API `get_logger` compatível e alternável por feature flag até a migração total.
  - Remover `structlog` ao final.

---

### 2) Tracing: manter OTEL opcional e integrar ao logging
- **Estado atual**: `app/infra/tracing.py` com wrapper opcional para OpenTelemetry.
- **Proposta**:
  - Preservar `start_span` no-op quando desativado.
  - Superfície mínima: `configure`, `start_span`, `current_trace_ids`.
  - Injetar `trace_id`/`span_id` no logging via `contextvars` e formatter stdlib.
- **Benefícios**: integração simples com logging, menos acoplamento.
- **Esforço**: baixo (0.5–1h).

---

### 3) Config: consolidar em `app.config.settings.Settings`
- **Estado atual**: coexistem `ConfigLoader/get_config` e `Settings/get_settings` (Pydantic v2) com merge e substituição `${VAR:-default}` manuais.
- **Problema**: duplicação e superfície maior de manutenção.
- **Proposta**:
  - Padronizar consumo por `get_settings()`; aposentar `ConfigLoader/get_config` e chamadas.
  - Usar capacidades nativas do Pydantic Settings e leitura `yaml.safe_load` (substituição de env apenas onde necessário).
- **Benefícios**: tipagem, validação e override de env nativos.
- **Esforço**: médio (2–4h).
- **Passos**:
  - Mapear usos de `get_config` e migrar para `get_settings`.
  - Ajustar modelos/fields para cobrir chaves de `observability.yaml`, `agents.yaml`, `models.yaml`, `database.yaml`.

---

### 4) DB: remover engine global mutável; usar fábrica cacheada
- **Estado atual**: `_ENGINE` global em `app/infra/db.py` e mutação externa via `db._ENGINE = engine` em `app/graph/assistant.py`.
- **Problema**: difícil de testar, side effects e riscos em concorrência.
- **Proposta**:
  - `get_engine(dsn, ...)` com `functools.lru_cache` (determinístico, sem estado global exposto).
  - `open_connection()` delega ao engine cacheado; remover set externo.
  - Ponto de entrada chama `ensure_db()` idempotente.
- **Benefícios**: melhor testabilidade e isolamento.
- **Esforço**: médio (1–2h).

---

### 5) Validation: migrar para Pydantic models/schemas
- **Estado atual**: `app/utils/validation.py` oferece coercions e ensures.
- **Problema**: duplica funcionalidades nativas do Pydantic.
- **Proposta**:
  - Substituir validações em fluxo por modelos Pydantic (`BaseModel`, `Field`, `@field_validator`).
  - Manter apenas utilitários realmente gerais (ex.: `safe_limit`) caso não caibam em modelos.
- **Benefícios**: mensagens padronizadas, tipagem consistente.
- **Esforço**: médio (1–3h).

---

### 6) JSON helpers: preferir stdlib e otimização opcional
- **Estado atual**: `safe_json_dumps` usa `orjson` se disponível, fallback `json`.
- **Proposta**:
  - Usar `json.loads` diretamente onde possível; manter apenas `safe_json_dumps` como otimização opcional.
- **Esforço**: baixo.

---

### 7) Time utilities: reduzir API ao essencial
- **Estado atual**: `app/utils/time.py` oferece parsing/formatting ISO e helpers de tempo.
- **Proposta**:
  - Centralizar em `datetime.now(UTC)` e `time.monotonic()`; manter `has_expired/remaining_ms` por conveniência.
  - Usar `datetime.fromisoformat` quando aplicável.
- **Esforço**: baixo.

---

### 8) Typing extensions: usar `typing` quando possível
- **Estado atual**: aliases JSON, `SupportsToDict`, `is_json_compatible`.
- **Proposta**:
  - Manter aliases se agregarem legibilidade; evitar checagens runtime onde não necessárias.
- **Esforço**: baixo.

---

### 9) API server: simplificar fallbacks e montagem `/graph`
- **Estado atual**: `app/api/server.py` com múltiplos try/except e condicionais.
- **Proposta**:
  - Um único guard para indisponibilidade de FastAPI/LangGraph; logs via stdlib; `start_span` no-op.
  - Corrigir condicionais incompletos detectados durante a migração.
- **Esforço**: baixo.

---

### 10) Checkpointer: avaliar backend nativo do LangGraph
- **Estado atual**: `app/infra/checkpointer.py` com wrapper Postgres e no-op.
- **Proposta**:
  - Adotar checkpointers oficiais (FS/SQLite/Postgres) se compatíveis, configurados via `Settings`.
- **Benefícios**: menos manutenção e aderência ao ecossistema.
- **Esforço**: baixo–médio.

---

### 11) LLM backends: centralizar cliente e parsing JSON
- **Estado atual**: parsing JSON repetido em agentes (e.g., Analytics/Router).
- **Proposta**:
  - Cliente LLM compartilhado com timeout, retries (stdlib) e extração JSON consistente.
- **Benefícios**: menos duplicação e comportamento uniforme.
- **Esforço**: médio.

---

### 12) Limpeza e correções pontuais
- **Proposta**:
  - Remover código morto/duplicado.
  - Corrigir condicionais truncadas e retornos faltantes onde identificados.

---

### Plano de implementação (ordem sugerida)
1. Logging stdlib-only com feature flag; migrar imports e remover structlog.
2. Tracing integrado ao logging via `contextvars`; manter OTEL opcional.
3. Consolidar config em `Settings`; remover `ConfigLoader/get_config`.
4. Refatorar DB engine para fábrica cacheada; remover mutação global.
5. Migrar validações para Pydantic models/schemas.
6. Limpar JSON/time/typing helpers (stdlib-first, minimal).
7. Simplificar API server fallbacks e montagem `/graph`.
8. Avaliar checkpointer nativo LangGraph.
9. Consolidar LLM backend para parsing/retries unificado.

### Impacto esperado
- **Menos dependências** e menor superfície de manutenção.
- **Observabilidade padronizada** e previsível (logging/tracing nativos).
- **Melhor testabilidade** (DB sem estado global mutável; validações tipadas).

### Métricas de sucesso (sugestão)
- Redução de dependências (p.ex., remoção de `structlog`).
- Cobertura de logs consistente (campos de contexto presentes) e sem regressões.
- Testes de inicialização sem side effects globais.
- Menor quantidade de helpers custom usados em novas mudanças.


