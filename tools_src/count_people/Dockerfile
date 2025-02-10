FROM python:3.12 AS builder

RUN pip install poetry==1.8

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.12-slim AS runtime

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libgl1-mesa-glx

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ENV PICTURAS_LOG_LEVEL=WARN

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY count_people_tool_ms ./count_people_tool_ms

ENTRYPOINT ["python", "-m", "count_people_tool_ms.main"]
