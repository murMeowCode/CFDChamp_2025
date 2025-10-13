"""Продюсер для пользовательских событий"""#pylint:disable=E0401
import logging
from shared.messaging.producers import BaseProducer
from shared.schemas.messaging import UserCreatedMessage

logger = logging.getLogger(__name__)

class UserProducer(BaseProducer):
    """Продюсер для отправки событий связанных с пользователями"""

    def __init__(self, rabbitmq_url: str, exchange_name: str = "auth_exchange"):
        super().__init__(rabbitmq_url, exchange_name)

    async def send_user_created_event(self, message: UserCreatedMessage):
        """Отправляет событие создания пользователя"""
        await self._send_message(
            message=message,
            routing_key="auth.user.created"  # или "auth.user.created" в зависимости от вашей маршрутизации
        )
        logger.info(f"User created event sent for user_id: {message.user_id}")
