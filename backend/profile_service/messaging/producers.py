import aio_pika
import json
import uuid
from shared.messaging.base import RabbitMQBase
from profile_service.schemas.messaging import BaseMessage, MessageType, TokenVerifyResponseMessage
import logging

logger = logging.getLogger(__name__)

class AuthProducer(RabbitMQBase):
    def __init__(self, rabbitmq_url: str):
        super().__init__(rabbitmq_url)
        self.exchange_name = "auth_exchange"

    async def connect(self):
        await super().connect()
        self.exchange = await self.channel.declare_exchange(
            name=self.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

    async def verify_token(self, token: str, timeout: int = 5) -> TokenVerifyResponseMessage:
        """Отправляет запрос на верификацию токена и ждет ответ"""
        correlation_id = str(uuid.uuid4())
        
        # Создаем временную очередь для ответа
        reply_queue = await self.channel.declare_queue(
            name=f"auth.verify.reply.{correlation_id}",
            durable=False,
            auto_delete=True,
            exclusive=True
        )

        # Создаем сообщение
        verify_message = BaseMessage(
            message_type=MessageType.TOKEN_VERIFY_REQUEST,
            data={"token": token},
            correlation_id=correlation_id,
            reply_to=reply_queue.name
        )

        # Отправляем запрос
        message = aio_pika.Message(
            body=json.dumps(verify_message.model_dump()).encode(),
            content_type="application/json",
            correlation_id=correlation_id,
            reply_to=reply_queue.name
        )

        await self.exchange.publish(
            message,
            routing_key="auth.verify.request"
        )

        logger.info(f"Token verification request sent: {correlation_id}")

        # Ждем ответ
        async with reply_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if message.correlation_id == correlation_id:
                        data = json.loads(message.body.decode())
                        response = TokenVerifyResponseMessage(**data["data"])
                        logger.info(f"Token verification response received: {response.valid}")
                        return response

        # Таймаут
        raise TimeoutError("Token verification timeout")
