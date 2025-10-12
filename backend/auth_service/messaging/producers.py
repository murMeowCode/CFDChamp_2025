"""модкль продюсера""" #pylint: disable=E0401, W1203, W0707
import json
import uuid
import logging
import aio_pika
from shared.messaging.producers import BaseProducer
from shared.schemas.messaging import BaseMessage, MessageType, TokenVerifyResponseMessage

logger = logging.getLogger(__name__)

class AuthProducer(BaseProducer):
    """Продюсер для сервиса аутентификации с RPC-функциональностью"""

    def __init__(self, rabbitmq_url: str):
        super().__init__(rabbitmq_url, "auth_exchange")

    async def verify_token(self, token: str, timeout: int = 30) -> TokenVerifyResponseMessage:
        """Отправляет RPC-запрос на верификацию токена и ждет ответ"""
        correlation_id = str(uuid.uuid4())

        # Создаем временную очередь для ответа
        reply_queue = await self.channel.declare_queue(
            name=f"auth.verify.reply.{correlation_id}",
            durable=False,
            auto_delete=True,
            exclusive=True
        )

        # Создаем сообщение запроса
        verify_message = BaseMessage(
            message_type=MessageType.TOKEN_VERIFY_REQUEST,
            data={"token": token},
            correlation_id=correlation_id,
            reply_to=reply_queue.name
        )

        # Отправляем запрос
        await self._send_message(
            message=verify_message,
            routing_key="auth.verify.request",
            correlation_id=correlation_id,
            reply_to=reply_queue.name
        )

        logger.info(f"Token verification request sent: {correlation_id}")

        # Ждем ответ с таймаутом
        try:
            async with reply_queue.iterator(timeout=timeout) as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        if message.correlation_id == correlation_id:
                            data = json.loads(message.body.decode())
                            response = TokenVerifyResponseMessage(**data["data"])
                            logger.info(f"Token verification response received: {response.valid}")
                            return response

            raise TimeoutError("No response received within timeout")

        except aio_pika.exceptions.QueueEmpty:
            raise TimeoutError("Token verification timeout - no response received")
