"""Потребитель RabbitMQ для сервиса рассылки"""  # pylint: disable=W1203, E0401, W0718
import json
import logging
import aio_pika
from shared.messaging.consumers import BaseConsumer
from shared.database.database import AsyncSessionLocal
from mailing_service.services.email_service import email_service
from mailing_service.schemas.message import EmailData
from mailing_service.services.message_service import MessageService


logger = logging.getLogger(__name__)

class MailingConsumer(BaseConsumer):
    """Потребитель для обработки уведомлений и отправки email"""

    def __init__(self, rabbitmq_url: str, exchange_name: str = "auth_exchange"):
        super().__init__(rabbitmq_url, exchange_name)
        self.queue_name = "mailing_queue"

    async def setup_queues(self):
        """Настройка очередей для mailing service"""
        # Основная очередь для уведомлений
        queue = await self.declare_and_bind_queue(
            queue_name=self.queue_name,
            routing_key="notification.*"
        )

        # Начинаем слушать очередь
        await queue.consume(self.handle_notification)
        logger.info(f"MailingConsumer started listening on queue: {self.queue_name}")

    async def handle_notification(self, message: aio_pika.IncomingMessage):
        """Обработка входящих уведомлений"""
        success = await self.process_message(message, self._process_notification)
        if success:
            logger.info("Notification processed successfully")
        else:
            logger.error("Failed to process notification")

    async def _process_notification(self, message: aio_pika.IncomingMessage):
        """Основная логика обработки уведомления"""
        # Парсим сообщение
        body = json.loads(message.body.decode())
        logger.info(f"Received notification: {body}")

        # Определяем тип уведомления и обрабатываем
        notification_type = body.get("type")
        user_email = body.get("user_email")
        user_id = body.get("user_id")
        data = body.get("data", {})

        if not user_email or not user_id:
            logger.error("No user_email or user_id in notification")
            return

        # Создаем запись в базе данных
        async with AsyncSessionLocal() as session:
            message_service = MessageService(session)

            # Создаем запись сообщения
            message_record = await message_service.create_message(
                user_id=user_id,
                subject=self._get_subject_by_type(notification_type, data),
                content=self._get_content_by_type(notification_type, data)
            )

            logger.info(f"Message record created with ID: {message_record.id}")

        # Отправляем email
        await self._send_email_by_type(notification_type, user_email, data)

    async def _send_email_by_type(self, notification_type: str, user_email: str, data: dict):
        """Отправка email в зависимости от типа уведомления"""
        handlers = {
            "user_registered": self._handle_user_registered,
            "welcome_message": self._handle_welcome_message,
            "custom_notification": self._handle_custom_notification
        }

        handler = handlers.get(notification_type)
        if handler:
            await handler(user_email, data)
        else:
            logger.warning(f"Unknown notification type: {notification_type}")

    def _get_subject_by_type(self, notification_type: str, data: dict) -> str:
        """Получение темы сообщения по типу уведомления"""
        subjects = {
            "user_registered": "Добро пожаловать в CFDChamp!",
            "welcome_message": "Приветственное сообщение от CFDChamp",
            "custom_notification": data.get("subject", "Уведомление от CFDChamp")
        }
        return subjects.get(notification_type, "Уведомление от CFDChamp")

    def _get_content_by_type(self, notification_type: str, data: dict) -> str:
        """Получение текста сообщения по типу уведомления"""
        username = data.get("username", "Пользователь")
        custom_content = data.get("content", "")

        contents = {
            "user_registered": f"Добро пожаловать, {username}! Спасибо за регистрацию в CFDChamp.",
            "welcome_message": f"Привет, {username}! Рады видеть вас в нашем сообществе трейдеров.",
            "custom_notification": custom_content or "У вас новое уведомление."
        }
        return contents.get(notification_type, "У вас новое уведомление.")

    async def _handle_user_registered(self, user_email: str, data: dict):
        """Обработка регистрации пользователя"""
        username = data.get("username", "Пользователь")

        email_data = EmailData(
            to=[user_email],
            subject="Добро пожаловать в CFDChamp!",
            html=self._create_welcome_template(username)
        )

        await email_service.send_email(email_data)
        logger.info(f"Welcome email sent to {user_email}")

    async def _handle_welcome_message(self, user_email: str, data: dict):
        """Обработка приветственного сообщения"""
        username = data.get("username", "Пользователь")

        email_data = EmailData(
            to=[user_email],
            subject="Приветственное сообщение от CFDChamp",
            html=self._create_welcome_template(username, is_extended=True)
        )

        await email_service.send_email(email_data)
        logger.info(f"Extended welcome email sent to {user_email}")

    async def _handle_custom_notification(self, user_email: str, data: dict):
        """Обработка кастомных уведомлений"""
        subject = data.get("subject", "Уведомление от CFDChamp")
        content = data.get("content", "")

        email_data = EmailData(
            to=[user_email],
            subject=subject,
            html=self._create_custom_template(content)
        )

        await email_service.send_email(email_data)
        logger.info(f"Custom notification sent to {user_email}")

    def _create_welcome_template(self, username: str, is_extended: bool = False) -> str:
        """Шаблон приветственного письма"""
        if is_extended:
            return f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #4F46E5;">Добро пожаловать в CFDChamp, {username}!</h1>
                    <p>Мы рады приветствовать вас в нашем сообществе трейдеров.</p>
                    <p>Теперь у вас есть доступ ко всем возможностям нашей платформы:</p>
                    <ul>
                        <li>Анализ CFD инструментов</li>
                        <li>Торговые сигналы</li>
                        <li>Образовательные материалы</li>
                    </ul>
                    <p>Если у вас есть вопросы, не стесняйтесь обращаться в поддержку.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        С уважением,<br>Команда CFDChamp
                    </p>
                </div>
            </body>
            </html>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4F46E5;">Добро пожаловать, {username}!</h2>
                <p>Спасибо за регистрацию в CFDChamp.</p>
                <p>Начните знакомство с платформой прямо сейчас!</p>
            </div>
        </body>
        </html>
        """

    def _create_custom_template(self, content: str) -> str:
        """Шаблон для кастомных уведомлений"""
        return f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px;">
                    {content}
                </div>
                <p style="color: #666; font-size: 12px; margin-top: 20px;">
                    С уважением,<br>Команда CFDChamp
                </p>
            </div>
        </body>
        </html>
        """
