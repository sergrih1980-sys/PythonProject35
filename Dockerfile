FROM python:3.13-slim

WORKDIR /app

# Системные зависимости (нужны и для beat, если есть общие libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем файлы зависимостей (обязательно оба)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Копируем код проекта
COPY . .

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

# Команда запуска именно Celery Beat
CMD ["celery", "-A", "config", "beat", "--loglevel=info"]