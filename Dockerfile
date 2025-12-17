# --------------------------------------------------------
# ETAPA 1 - Base con Poetry
# --------------------------------------------------------
FROM python:3.12-slim AS base

WORKDIR /app

# Instalar wget y dependencias básicas
RUN apt-get update && apt-get install -y wget procps

# Instalar poetry
RUN pip install poetry && poetry config virtualenvs.create false


# --------------------------------------------------------
# ETAPA 2 - Desarrollo
# --------------------------------------------------------
FROM base AS development

# Solo copiamos pyproject
COPY pyproject.toml ./

# Generamos lockfile dentro del contenedor
RUN poetry lock --no-interaction

# Instalamos dependencias
RUN poetry install --no-interaction --no-root

# Copiamos código
COPY . .

ENV PYTHONPATH=/app

CMD ["poetry", "run", "uvicorn", "app.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8800", "--reload"]


# --------------------------------------------------------
# ETAPA 3 - Producción
# --------------------------------------------------------
FROM base AS production

# Copiamos pyproject y lock (generado por dev/prod build)
COPY pyproject.toml ./
RUN poetry lock --no-interaction
RUN poetry install --no-interaction --no-root

# Copiamos solo el código necesario
COPY app ./app

ENV PYTHONPATH=/app

CMD ["poetry", "run", "uvicorn", "app.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

