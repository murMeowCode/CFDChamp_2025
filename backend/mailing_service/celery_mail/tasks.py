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
    logger.info("🎬 STARTING Celery task process_notification_task")
    logger.info(f"📦 Task ID: {self.request.id}")
    logger.info(f"📊 Notification data keys: {list(notification_data.keys())}")
    logger.info(f"👤 User ID: {notification_data.get('user_id', 'NOT_FOUND')}")
    logger.info(f"📧 User email: {notification_data.get('user_email', 'NOT_FOUND')}")

    try:
        logger.info("🚀 Starting async processing with asyncio.run()...")

        # asyncio.run() автоматически создает и управляет event loop
        result = asyncio.run(_process_notification_async(notification_data))

        logger.info(f"✅ SUCCESS - Notification processed. Message ID: {result}")
        return {"status": "success", "message_id": result}

    except Exception as exc:
        logger.error(f"💥 FAILED - Error in process_notification_task: {exc}")
        logger.exception("Detailed exception traceback:")

        retry_count = self.request.retries
        logger.warning(f"🔄 Retrying task... (attempt {retry_count + 1}/3)")

        raise self.retry(exc=exc, countdown=30)

async def _process_notification_async(notification_data: dict):
    """Асинхронная обработка уведомления"""
    logger.info("🔄 STARTING _process_notification_async")

    try:
        logger.info("🔌 Creating database session...")
        async with AsyncSessionLocal() as session:
            message_service = MessageService(session)

            logger.info("💾 Creating message record in database...")
            message_record = await message_service.create_message(
                user_id=notification_data["user_id"],
                subject=notification_data.get("subject", "Уведомление"),
                content=notification_data.get("content", "")
            )
            logger.info(f"✅ Message record created with ID: {message_record.id}")

            # Подготавливаем данные для email
            email_data = EmailData(
                to=[notification_data["user_email"]],
                subject=notification_data.get("subject", "Уведомление"),
                html=notification_data.get("html_content", "")
            )

            logger.info(f"📧 Preparing email to: {email_data.to}")
            logger.info(f"📝 Email subject: {email_data.subject}")

            logger.info("🚀 Sending email...")
            await email_service.send_email(email_data)
            logger.info("✅ Email sent successfully")

            logger.info(f"🏁COMPLETED _process_notification_async,returning ID:{message_record.id}")
            return message_record.id

    except Exception as e:
        logger.error(f"💥 ERROR in _process_notification_async: {e}")
        logger.exception("Detailed async processing exception:")
        raise
