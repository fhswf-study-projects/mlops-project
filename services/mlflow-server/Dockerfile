FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update -y && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry self add poetry-plugin-export

COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt