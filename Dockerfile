# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV EMBEDDED_FIREWORKS_KEY_PATH=/app/.captionman/final_fireworks_key

ARG RUNTIME_AI_PROVIDER=mock
ARG RUNTIME_OFFICIAL_MODE=false
ARG RUNTIME_MODEL_ROUTING_MODE=champion
ARG RUNTIME_CHAMPION_ROUTE=fireworks_kimi_glm
ARG RUNTIME_GEMMA_USAGE_MODE=off

ENV AI_PROVIDER=$RUNTIME_AI_PROVIDER
ENV OFFICIAL_MODE=$RUNTIME_OFFICIAL_MODE
ENV MODEL_ROUTING_MODE=$RUNTIME_MODEL_ROUTING_MODE
ENV CHAMPION_ROUTE=$RUNTIME_CHAMPION_ROUTE
ENV GEMMA_USAGE_MODE=$RUNTIME_GEMMA_USAGE_MODE
ENV REQUIRE_GEMMA_FOR_SUBMISSION=false
ENV FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1
ENV VISION_MODEL=accounts/fireworks/models/kimi-k2p6
ENV TEXT_MODEL=accounts/fireworks/models/glm-5p2
ENV JUDGE_MODEL=accounts/fireworks/models/glm-5p2
ENV GEMMA_MODEL=accounts/fireworks/models/gemma-4-31b-it
ENV CAPTION_CANDIDATES_PER_STYLE=1
ENV NUM_FRAMES=6
ENV MIN_FRAMES=4
ENV MAX_FRAMES=8
ENV MAX_MODEL_CALLS_PER_VIDEO=6

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY apps/api/pyproject.toml apps/api/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY apps/api/app ./app
COPY prompts ./prompts
COPY README.md ./README.md

RUN uv sync --frozen --no-dev

ARG ALLOW_EMBEDDED_HACKATHON_KEY=false
RUN --mount=type=secret,id=fireworks_api_key,required=false \
    set -eu; \
    if [ "$ALLOW_EMBEDDED_HACKATHON_KEY" = "true" ]; then \
        if [ "$AI_PROVIDER" != "fireworks_direct" ]; then \
            echo "Embedded-key final images must set RUNTIME_AI_PROVIDER=fireworks_direct" >&2; \
            exit 1; \
        fi; \
        if [ "$OFFICIAL_MODE" != "true" ]; then \
            echo "Embedded-key final images must set RUNTIME_OFFICIAL_MODE=true" >&2; \
            exit 1; \
        fi; \
        if [ ! -f /run/secrets/fireworks_api_key ]; then \
            echo "ALLOW_EMBEDDED_HACKATHON_KEY=true requires BuildKit secret id=fireworks_api_key" >&2; \
            exit 1; \
        fi; \
        mkdir -p /app/.captionman; \
        cp /run/secrets/fireworks_api_key "$EMBEDDED_FIREWORKS_KEY_PATH"; \
        chmod 0400 "$EMBEDDED_FIREWORKS_KEY_PATH"; \
    elif [ "$ALLOW_EMBEDDED_HACKATHON_KEY" = "false" ]; then \
        if [ -f /run/secrets/fireworks_api_key ]; then \
            echo "Refusing to embed fireworks_api_key without ALLOW_EMBEDDED_HACKATHON_KEY=true" >&2; \
            exit 1; \
        fi; \
        rm -rf /app/.captionman; \
    else \
        echo "ALLOW_EMBEDDED_HACKATHON_KEY must be true or false" >&2; \
        exit 1; \
    fi

ENV PATH="/app/.venv/bin:$PATH"

RUN captionman --help

CMD ["captionman", "run", "--input", "/input/tasks.json", "--output", "/output/results.json"]
