# syntax=docker/dockerfile:1

###############################################################################
# Stage 1: builder — resolve and install dependencies into an isolated venv
###############################################################################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# uv build-time tuning:
# - bytecode compile for faster cold starts
# - copy (not hardlink) deps so the venv is self-contained for the runtime stage
# - never try to download a managed Python; use the image's interpreter
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install dependencies first (cached layer) using only the lock + manifest.
# A cache mount keeps uv's wheel cache warm across builds without bloating layers.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Now copy the source and install the project itself (editable-free, into the venv).
# This second sync only re-runs when src/ changes, keeping dependency layers cached.
COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

###############################################################################
# Stage 2: runtime — minimal image, non-root, venv + source only
###############################################################################
FROM python:3.12-slim-bookworm AS runtime

# Runtime hygiene: no .pyc churn, unbuffered logs, venv on PATH.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

# Create an unprivileged user/group to run the app.
RUN groupadd --system --gid 1000 app \
    && useradd --system --uid 1000 --gid app --no-create-home --home-dir /app app

WORKDIR /app

# Bring over the fully-built virtualenv and the application code.
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app src/ ./src/
COPY --chown=app:app migrations/ ./migrations/
COPY --chown=app:app alembic.ini ./alembic.ini

USER app

EXPOSE 8000

# Default entrypoint is the API. docker-compose overrides this with `run-worker`
# for the consumer service via the `command:` field.
CMD ["run-api"]
