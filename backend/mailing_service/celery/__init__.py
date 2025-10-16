"""Инициализация Celery"""
from celery import Celery
from mailing_service.celery.config import CeleryConfig

# Создаем экземпляр Celery
celery_app = Celery("mailing_service")

# Загружаем конфигурацию
celery_app.config_from_object(CeleryConfig)

# Автоматически обнаруживаем задачи
celery_app.autodiscover_tasks(["mailing_service.celery.tasks"])

# Отладочная информация
print(f"Celery broker: {celery_app.conf.broker_url}")
