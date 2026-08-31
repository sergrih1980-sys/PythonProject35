FROM python:3.13-slim

WORKDIR /app

# Системные зависимости: libpq-dev (psycopg2), gcc (бинарные расширения), libjpeg/zlib (Pillow)
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

# Копируем только файлы зависимостей для кэширования слоя
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости проекта (production)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Теперь копируем весь код проекта
COPY . .

# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

# Порт для Gunicorn внутри контейнера
EXPOSE 8000

# Команда по умолчанию будет переопределена в docker-compose.yml
# Оставляем её как fallback
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Gunicorn нужен для запуска Django в контейнере
RUN pip install gunicorn