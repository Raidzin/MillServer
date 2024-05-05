FROM python:3.12-slim as builder
LABEL authors="Raidzin"

WORKDIR /millserver

RUN python -m pip install --no-cache-dir poetry==1.8.2 \
    && poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-interaction --no-ansi

FROM python:3.12-slim

WORKDIR /millserver

COPY --from=builder /millserver /millserver

COPY millserver /millserver

ENV PYTHONPATH=/millserver

ENTRYPOINT [".venv/bin/python", "-m"]

CMD ["granian", "main:app", "--interface", "asgi", "--host", "0.0.0.0"]
