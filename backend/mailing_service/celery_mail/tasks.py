"""задачи для Celery""" #pylint: disable=E0401, W1203
import logging
import asyncio
from mailing_service.celery_mail import celery_app
from shared.database.database import AsyncSessionLocal
from mailing_service.services.email_service import email_service
from mailing_service.services.message_service import MessageService
from mailing_service.schemas.message import EmailData

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def process_notification_task(self, notification_data: dict):
    """Задача для обработки уведомления и отправки email"""
    try:

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            _process_notification_async(notification_data)
        )

        return {"status": "success", "message_id": result}

    except Exception as exc:
        logger.error(f"Failed to process notification: {exc}")
        raise self.retry(exc=exc, countdown=30)

async def _process_notification_async(notification_data: dict):
    """Асинхронная обработка уведомления"""
    async with AsyncSessionLocal() as session:
        message_service = MessageService(session)

        # Создаем запись в базе данных
        message_record = await message_service.create_message(
            user_id=notification_data["user_id"],
            subject=notification_data.get("subject", "Уведомление"),
            content=notification_data.get("content", "")
        )

        # Подготавливаем данные для email
        email_data = EmailData(
            to=[notification_data["user_email"]],
            subject=notification_data.get("subject", "Уведомление"),
            html=notification_data.get("html_content", "")
        )

        # Отправляем email
        await email_service.send_email(email_data)

        return message_record.id
