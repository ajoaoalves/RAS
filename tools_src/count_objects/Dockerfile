# Etapa de construção
FROM python:3.12 AS builder

# Instala o Poetry
RUN pip install poetry==1.8

# Configurações do Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários para instalar as dependências
COPY pyproject.toml poetry.lock ./

# Instala as dependências sem instalar o próprio projeto
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

# Etapa de execução
FROM python:3.12-slim AS runtime

# Instala dependências do sistema para lidar com imagens e OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends libglib2.0-0 libgl1-mesa-glx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configurações de ambiente
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PICTURAS_LOG_LEVEL=WARN

# Copia o ambiente virtual criado na etapa de construção
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copia o código da aplicação
COPY count_objects_tool_ms ./count_objects_tool_ms

# Define o ponto de entrada para o contêiner
ENTRYPOINT ["python", "-m", "count_objects_tool_ms.main"]
