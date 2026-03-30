FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy only what the app needs
COPY base_config.py base_config.py
COPY src/services/event_scanner src/services/event_scanner
COPY src/libs/common src/libs/common
COPY src/libs/geolocation src/libs/geolocation
COPY src/libs/lastfm src/libs/lastfm
COPY src/libs/podiuminfo src/libs/podiuminfo
COPY src/libs/spotify src/libs/spotify

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:/app/src"

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/base_config.py /app/base_config.py
COPY --from=builder /app/src /app/src

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python3", "/app/src/services/event_scanner/nicegui_ui/main.py"]