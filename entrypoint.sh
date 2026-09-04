#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! python -c "import socket; socket.create_connection(('db', 5432), timeout=2)" 2>/dev/null; do
  echo "PostgreSQL is not ready, waiting..."
  sleep 1
done
echo "PostgreSQL is up!"

# Миграции и collectstatic делаем только для Gunicorn (web), а не для worker/beat
if [ "$1" = "gunicorn" ]; then
  echo "Running migrations..."
  python manage.py migrate --noinput
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

exec "$@"