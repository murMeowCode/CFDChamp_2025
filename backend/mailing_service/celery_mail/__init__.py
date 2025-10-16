"""Инициализация Celery""" #pylint: disable=W0406, E0401, W1203, C0413
import logging
import os
import sys
from celery import Celery

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.config.base import settings

logger = logging.getLogger(__name__)

# Создаем экземпляр Celery
celery_app = Celery("mailing_service")

celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
)

# Отладочный вывод
logger.info(f"Celery broker URL: {celery_app.conf.broker_url}")
logger.info(f"Celery result backend: {celery_app.conf.result_backend}")

# Автоматически обнаруживаем задачи
celery_app.autodiscover_tasks(["mailing_service.celery_mail.tasks"])
