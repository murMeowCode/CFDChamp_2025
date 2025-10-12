# profile_service/messaging/consumers.py
import json
import logging
import aio_pika
from shared.messaging.consumers import BaseConsumer
from shared.schemas.messaging import UserCreatedMessage
from profile_service.services.service import ProfileService

logger = logging.getLogger(__name__)

class ProfileConsumer(BaseConsumer):
    """Потребитель для обработки событий профилей"""
    
    def __init__(self, rabbitmq_url: str, profile_service: ProfileService):
        super().__init__(rabbitmq_url, "auth_exchange")
        self.profile_service = profile_service

    async def setup_queues(self):
        """Настройка очередей для событий профилей"""
        # Очередь для создания пользователей
        user_created_queue = await self.declare_and_bind_queue(
            queue_name="auth.user.created",
            routing_key="auth.user.created"
        )
        await user_created_queue.consume(
            lambda msg: self.process_message(msg, self._handle_user_created)
        )
        
        logger.info("ProfileConsumer queues setup completed")

    async def _handle_user_created(self, message: aio_pika.IncomingMessage):
        """Обрабатывает сообщение о создании пользователя"""
        data = json.loads(message.body.decode())
        user_message = UserCreatedMessage(**data)

        logger.info(f"Received user created event for user_id: {user_message.user_id}")

        # Создаем профиль из данных пользователя
        profile_data = {
            "user_id": user_message.user_id,
            "first_name": user_message.first_name,
            "last_name": user_message.last_name,
            "middle_name": user_message.middle_name,
            "birth_date": user_message.birth_date,
            "phone": user_message.phone,
            "address": user_message.address
        }

        # Создаем профиль
        profile = await self.profile_service.create_profile_from_message(profile_data)

        if profile:
            logger.info(f"Profile created successfully for user {user_message.user_id}")
        else:
            logger.error(f"Failed to create profile for user {user_message.user_id}")