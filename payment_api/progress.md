# Progress Log

## Summary
- Total tasks: 34
- Done: 5 (TASK-001, TASK-002, TASK-003, TASK-004, TASK-026)
- In progress: 0
- Pending: 29

**Next unblocked critical tasks**: TASK-005 (Payment model, depends on TASK-004 ✓), TASK-006 (OutboxMessage model, depends on TASK-004 ✓), TASK-008 (FastStream broker, depends on TASK-003 ✓), TASK-027/028/029 (TDD RED tests, depend on TASK-026 ✓)

---

## TASK-004 — Async SQLAlchemy: движок, async_sessionmaker, Base, get_session
- **Date**: 2026-05-28
- **Status**: done
- **What was done**:
  - Implemented `db/database.py` with SQLAlchemy 2.0 async pattern
  - `create_async_engine(settings.database_url, pool_pre_ping=True)` — engine created at module level
  - `async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)` — private `_session_factory`
  - `Base(DeclarativeBase)` — SQLAlchemy 2.0 style declarative base
  - `get_session() -> AsyncIterator[AsyncSession]` — async generator: commit on success, rollback on exception
  - `get_ro_session() -> AsyncIterator[AsyncSession]` — read-only dependency, no commit/rollback, use with `Depends(get_ro_session)` for GET endpoints
  - User removed `without_commit: bool = False` param from `get_session` in favour of the dedicated `get_ro_session` function
  - All test steps passed: import OK ✓, ruff clean ✓
- **Branch**: feature/TASK-004-async-sqlalchemy

---

<!-- Agents: append a new entry below after completing each task -->
<!-- Format:
## TASK-XXX — <task title>
- **Date**: YYYY-MM-DD
- **Status**: done
- **What was done**: <brief summary>
- **Issues encountered**: <any blockers or deviations from acceptance criteria>
- **Commits**: <commit hash(es)>
-->

## TASK-026 — Настройка pytest: конфигурация, conftest.py, TDD-инфраструктура
- **Date**: 2026-05-28
- **Status**: done
- **What was done**:
  - Added `log_cli = true` to `[tool.pytest.ini_options]` in pyproject.toml (asyncio_mode, testpaths, pythonpath were already present)
  - Created `tests/__init__.py` and `tests/unit/__init__.py`
  - Created `tests/conftest.py` with `mock_settings` fixture returning `Settings` with test values (TEST_API_KEY, fake postgres/rabbitmq URLs)
  - TDD smoke cycle: RED (`assert False`) → GREEN (`assert True`) → deleted smoke test
  - `uv run pytest --collect-only` exits 5 (no tests collected — expected, no errors) ✓, `ruff check tests/` exits 0 ✓
  - pytest-asyncio (1.4.0) and pytest-mock (3.15.1) already in dev dependencies ✓
- **Issues encountered**: None
- **Branch**: feature/TASK-026-pytest-setup

---

## TASK-003 — Конфигурация: Pydantic Settings в core/config.py
- **Date**: 2026-05-28
- **Status**: done
- **What was done**:
  - Implemented `Settings(BaseSettings)` with all 6 required fields: `database_url`, `rabbitmq_url`, `api_key (SecretStr)`, `outbox_poll_interval (int=5)`, `webhook_max_retries (int=3)`, `log_level (str='info')`
  - Added `model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")` — `extra="ignore"` is necessary because `.env` also contains Docker-specific vars (POSTGRES_USER, POSTGRES_PASSWORD, etc.) not declared in Settings; without it pydantic-settings raises ValidationError
  - `get_settings()` singleton via `@lru_cache` with return type `-> Settings`
  - All 3 test steps passed: fields present ✓, `api_key=SecretStr('**********')` hidden ✓, ruff clean ✓
  - python-expert review: implementation correct, no issues
- **Issues encountered**: `extra="ignore"` not in original AC spec but required due to Docker vars in `.env`
- **Branch**: feature/TASK-003-config
- **Commits**: pending git add

---

## TASK-002 — Скаффолдинг: структура src/payment_api/, заглушки модулей, entrypoint-ы
- **Date**: 2026-05-28
- **Status**: done
- **What was done**:
  - Created full `src/payment_api/` package structure with `__init__.py` in all subpackages: `api/v1/`, `consumer/`, `core/`, `db/models/`, `db/repositories/`, `domain/`, `schemas/`
  - Created stub modules with function/class-level `raise NotImplementedError` (not module-level, to allow imports): `core/config.py`, `core/security.py`, `core/broker.py`, `db/database.py`, `db/models/payment.py`, `db/models/outbox.py`, `db/repositories/payment.py`, `db/repositories/outbox.py`, `schemas/payment.py`, `api/v1/payments.py`, `api/router.py`, `consumer/worker.py`, `consumer/handler.py`, `domain/processor.py`, `domain/webhook.py`, `domain/outbox_service.py`, `domain/payment_service.py`, `main.py`
  - Added `anyio[trio]>=4.9.0` to dev dependencies in pyproject.toml
  - All test steps passed: `uv sync` ✓, `import payment_api` ✓, `ruff check src/` ✓, directory structure ✓
- **Issues encountered**: None. Stubs use function/class-level raises (not module-level) so imports never fail — this is the correct TDD pattern.
- **Next**: TASK-003 (Pydantic Settings в core/config.py) and TASK-026 (pytest setup) are both unblocked. TASK-026 depends only on TASK-002 and is critical priority — recommend doing it next. TASK-003 is also critical. Either can go first; TASK-026 sets up TDD infrastructure needed for TASK-027/028/029.
- **Commits**: ea4e4fb (base), this commit

---

## TASK-001 — Dev-окружение: Dockerfile, docker-compose.yml, Makefile, pyproject.toml, .env.example, alembic.ini
- **Date**: 2026-05-28
- **Status**: done
- **What was done**: Created all infrastructure files for the dev environment:
  - `Dockerfile`: multi-stage (uv builder + python:3.12-slim runtime), non-root app user, single image for api/worker
  - `docker-compose.yml`: postgres, rabbitmq (management port 15672), migrate, api, consumer; all with healthchecks; migrate uses `service_completed_successfully`; YAML anchor `x-app` for DRY config
  - `pyproject.toml`: uv-managed, hatchling build backend, all required dependencies, ruff with line-length=88, max-complexity=7, correct rule selects
  - `Makefile`: all 8 required targets (up, down, migrate, logs, test, lint, shell-api, shell-worker)
  - `alembic.ini`: script_location=migrations, sqlalchemy.url placeholder (overridden in env.py from DATABASE_URL)
  - `.env.example`: all 11 required vars with sensible defaults
  - `.gitignore`: ignores .venv, .env, __pycache__, etc.
  - `uv.lock` generated by running `uv run ruff check .`
- **Issues encountered**: Docker test steps (make up, compose ps, curl management UI) not run — requires live Docker/infra. All local verifiable steps passed: pyproject.toml valid TOML, docker-compose.yml valid YAML, `make lint` (uv run ruff check .) exits 0.
- **Next**: TASK-002 (scaffolding) — create src/payment_api/ package structure with stub modules. Run `make up` after TASK-002 to verify full Docker stack.
- **Commits**: (staged, not committed yet)
