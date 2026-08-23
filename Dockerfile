FROM python:3.13-slim

WORKDIR /app

# Системные зависимости: libpq-dev для psycopg2, gcc для бинарных расширений, libjpeg и libpng для Pillow
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

# Отключаем виртуальные окружения в контейнере
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

# Gunicorn нужен для запуска Django в контейнере
RUN pip install gunicorn