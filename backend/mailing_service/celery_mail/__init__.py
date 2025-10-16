"""Инициализация Celery""" #pylint: disable=W0406, E0401, W1203
import logging
from celery import Celery
from shared.config.base import settings

logger = logging.getLogger(__name__)

# Создаем экземпляр Celery
celery_app = Celery("mailing_service")

celery_app.conf.update(
    broker_url=f"redis://{settings.CELERY_BROKER_URL}",
    result_backend=f"redis://{settings.CELERY_RESULT_BACKEND}",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
)

# Отладочный вывод
logger.info(f"Celery broker URL: {celery_app.conf.broker_url}")
logger.info(f"Celery result backend: {celery_app.conf.result_backend}")

celery_app.autodiscover_tasks(["mailing_service.celery.tasks"])

# Автоматически обнаруживаем задачи
celery_app.autodiscover_tasks(["mailing_service.celery.tasks"])

# Отладочная информация
print(f"Celery broker: {celery_app.conf.broker_url}")
