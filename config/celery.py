import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Читаем настройки из Django settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит tasks.py во всех INSTALLED_APPS
app.autodiscover_tasks()