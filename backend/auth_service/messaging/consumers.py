"""класс для прослушивания очереди аутентификации"""#pylint: disable=E0401, W1203, W0718
from datetime import datetime
import json
import logging
from shared.messaging.base import RabbitMQBase
from shared.schemas.messaging import (
    BaseMessage, MessageType,
    TokenVerifyMessage
)
from auth_service.services.auth_service import AuthService
from auth_service.messaging.producers import AuthProducer
import aio_pika

logger = logging.getLogger(__name__)

class AuthConsumer(RabbitMQBase):
    """приемник очереди аутентификации"""
    def __init__(self, rabbitmq_url: str, auth_service: AuthService, producer: AuthProducer):
        super().__init__(rabbitmq_url)
        self.auth_service = auth_service
        self.producer = producer
        self.queues = {}

    async def connect(self):
        """осуществление подключения к очереди"""
        await super().connect()

        # Создаем exchange
        exchange = await self.channel.declare_exchange(
            name="auth_exchange",
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Очереди для auth запросов
        verify_queue = await self.channel.declare_queue(
            name="auth.verify.request",
            durable=True
        )
        await verify_queue.bind(exchange, routing_key="auth.verify.request")

        # Начинаем слушать очереди
        await verify_queue.consume(self._handle_verify_request)


    async def _handle_verify_request(self, message: aio_pika.IncomingMessage):
        """Обработка запроса верификации токена"""
        start_time = datetime.utcnow()
        message_id = message.correlation_id or f"msg_{start_time.timestamp()}"

        async with message.process():
            try:
                # Декодирование сообщения
                body = json.loads(message.body.decode())
                base_message = BaseMessage(**body)

                if base_message.message_type != MessageType.TOKEN_VERIFY_REQUEST:
                    return

                # Обработка верификации токена
                verify_message = TokenVerifyMessage(**base_message.data)

                response = await self.auth_service.verify_token_handler(verify_message)

                # Подготовка и отправка ответа
                response_message = BaseMessage(
                    message_type=MessageType.TOKEN_VERIFY_RESPONSE,
                    data=response.model_dump()
                )

                if base_message.reply_to:
                    await self.producer.send_response(
                        response_message,
                        base_message.reply_to,
                        base_message.correlation_id
                    )
                else:
                    logger.warning("⚠️ No reply queue specified", extra={"message_id": message_id})

                # Логирование завершения обработк
            except json.JSONDecodeError as e:
                logger.error("❌ JSON decode failed", extra={
                    "message_id": message_id,
                    "error": str(e),
                    "message_body_preview": message.body.decode()[:100] + "..." if message.body
                    else "Empty"
                })

            except Exception as e:
                logger.error("❌ Processing failed", extra={
                    "message_id": message_id,
                    "error": str(e),
                    "error_type": type(e).__name__
                })
                logger.exception("🔧 Exception details")
