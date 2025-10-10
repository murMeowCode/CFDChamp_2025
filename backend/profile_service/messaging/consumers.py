import aio_pika
import json
from shared.messaging.base import RabbitMQBase
from profile_service.schemas.messaging import UserCreatedMessage
from profile_service.services.service import ProfileService
import logging

logger = logging.getLogger(__name__)

class ProfileConsumer(RabbitMQBase):
    def __init__(self, rabbitmq_url: str, profile_service: ProfileService):
        super().__init__(rabbitmq_url)
        self.profile_service = profile_service

    async def connect(self):
        await super().connect()
        
        # Используем существующий exchange
        exchange = await self.channel.declare_exchange(
            name="auth_exchange",  # или какое имя используется
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Получаем ссылку на существующую очередь
        user_created_queue = await self.channel.declare_queue(
            name="auth.user.created",  # используем существующее имя
            durable=True
        )

        # Начинаем слушать существующую очередь
        await user_created_queue.consume(self._handle_user_created)

        logger.info("ProfileConsumer started listening for auth.user.created events")

    async def _handle_user_created(self, message: aio_pika.IncomingMessage):
        """Обрабатывает сообщение о создании пользователя"""
        async with message.process():
            try:
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

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in user.created handler: {e}")
            except Exception as e:
                logger.error(f"Error handling user.created event: {e}")