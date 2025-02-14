FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install poetry
RUN poetry self add poetry-plugin-export

# Install Dependencies
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy Project
COPY . .
