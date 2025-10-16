"""Конфигурация Celery для сервиса рассылки"""
from shared.config.base import settings #pylint: disable=E0401

class CeleryConfig:
    """Конфигурация Celery"""
    
    broker_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_CELERY}"
    result_backend = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_CELERY}"

    # Настройки задач
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "Europe/Moscow"
    enable_utc = True

    # Настройки воркера
    worker_prefetch_multiplier = 1
    task_acks_late = True
    worker_max_tasks_per_child = 1000

    # Роутинг задач
    task_routes = {
        "mailing_service.celery.tasks.send_email_task": {"queue": "mailing_queue"},
        "mailing_service.celery.tasks.process_notification_task": {"queue": "mailing_queue"},
    }

    # Расписание задач (если понадобится)
    beat_schedule = {}
