FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y libpq-dev python-dev gcc libc-dev g++

WORKDIR /app

COPY pyproject.toml /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .
