"""задачи для Celery (синхронные)""" #pylint: disable=E0401, W1203
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from shared.config.base import settings
from mailing_service.celery_mail import celery_app
from mailing_service.services.email_service import email_service_sync
from mailing_service.schemas.message import EmailData

logger = logging.getLogger(__name__)

# Создаем синхронный engine для Celery
sync_engine = create_engine(settings.DATABASE_URL.replace("asyncpg", "psycopg2"))

def get_sync_db():
    """Синхронная сессия для Celery"""
    db = Session(sync_engine)
    try:
        yield db
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def process_notification_task(self, notification_data: dict):
    """Синхронная задача для обработки уведомления и отправки email"""
    logger.info("🎬 STARTING Celery task process_notification_task")
    logger.info(f"📦 Task ID: {self.request.id}")
    logger.info(f"📊 Notification data keys: {list(notification_data.keys())}")
    logger.info(f"👤 User ID: {notification_data.get('user_id', 'NOT_FOUND')}")
    logger.info(f"📧 User email: {notification_data.get('user_email', 'NOT_FOUND')}")

    db = None
    try:
        # Используем синхронную сессию
        db = next(get_sync_db())

        # Подготавливаем данные для email
        email_data = EmailData(
            to=[notification_data["user_email"]],
            subject=notification_data.get("subject", "Уведомление"),
            html=notification_data.get("html_content", "")
        )
        logger.info(f"📝 Email subject: {email_data.subject}")

        logger.info("🚀 Sending email...")
        email_sent = email_service_sync.send_email(email_data)

        if email_sent:
            logger.info("✅ Email sent successfully")
        else:
            logger.error("❌ Failed to send email")

        logger.info(f"🏁 COMPLETED process_notification_task, returning ID: {self.request.id}")
        return {"status": "success", "email_sent": email_sent}

    except Exception as exc:
        logger.error(f"💥 FAILED - Error in process_notification_task: {exc}")
        logger.exception("Detailed exception traceback:")

        if db:
            db.rollback()

        retry_count = self.request.retries
        logger.warning(f"🔄 Retrying task... (attempt {retry_count + 1}/3)")
        raise self.retry(exc=exc, countdown=30)

    finally:
        if db:
            db.close()
