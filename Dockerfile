FROM python:3.11.13-slim-bullseye
LABEL org.opencontainers.image.source="https://github.com/amps-kt/matching-service"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN groupadd matching
RUN adduser --system --no-create-home --disabled-password --shell /bin/bash matching

WORKDIR /app

COPY pyproject.toml uv.lock .python-version .
RUN uv sync --frozen --no-cache

COPY . .

USER matching
CMD ["uv", "run", "--frozen", "--no-cache", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
