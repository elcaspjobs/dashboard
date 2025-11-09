FROM python:3.13-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    pkg-config \
    libzstd-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml .

RUN uv pip install --system -r pyproject.toml

COPY src ./src
COPY tests ./tests

