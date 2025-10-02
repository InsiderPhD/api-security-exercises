# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/home/appuser/.local/bin:$PATH"

# Create user and workdir
RUN useradd -ms /bin/bash appuser
WORKDIR /app

# System deps (build essentials may be unnecessary; keeping minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app /app/app

# Create data directory for SQLite database
RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser
EXPOSE 5000

# Default environment (can be overridden)
ENV HOST=0.0.0.0 \
    PORT=5000 \
    DB_PATH=/app/data/app.db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
