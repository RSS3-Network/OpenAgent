FROM python:3.11-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root
COPY . /app
ENV PYTHONPATH=/app
CMD ["poetry", "run", "python", "main.py"]
