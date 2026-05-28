COMPOSE := docker compose

.DEFAULT_GOAL := help
.PHONY: help up down migrate logs test lint shell-api shell-worker

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

up: ## Build and start the full stack in the background
	$(COMPOSE) up -d --build

down: ## Stop the stack and remove volumes
	$(COMPOSE) down --volumes --remove-orphans

migrate: ## Run alembic migrations to head against the running DB
	$(COMPOSE) run --rm migrate

logs: ## Tail logs from all services
	$(COMPOSE) logs -f --tail=100

test: ## Run the test suite locally via uv
	uv run pytest

lint: ## Lint and check formatting via ruff
	uv run ruff check .
	uv run ruff format --check .

shell-api: ## Open an interactive shell in the api container
	$(COMPOSE) exec api /bin/bash

shell-worker: ## Open an interactive shell in the consumer container
	$(COMPOSE) exec consumer /bin/bash
