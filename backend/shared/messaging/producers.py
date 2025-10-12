"""общий модуль для продюсеров"""#pylint: disable=E0401, W1203
import logging
import aio_pika
from shared.messaging.base import RabbitMQBase
from shared.schemas.messaging import BaseMessage

logger = logging.getLogger(__name__)

class BaseProducer(RabbitMQBase):
    """Базовый класс для всех продюсеров RabbitMQ"""

    def __init__(self, rabbitmq_url: str, exchange_name: str = "auth_exchange"):
        super().__init__(rabbitmq_url)
        self.exchange_name = exchange_name
        self.exchange: aio_pika.Exchange = None

    async def connect(self):
        """Подключение к RabbitMQ и настройка exchange"""
        await super().connect()
        self.exchange = await self.channel.declare_exchange(
            name=self.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        logger.info(f"{self.__class__.__name__} connected to exchange '{self.exchange_name}'")

    async def _send_message(self, message: BaseMessage, routing_key: str, **message_kwargs):
        """Базовый метод отправки сообщений"""
        if not self.exchange:
            await self.connect()

        # Создаем RabbitMQ сообщение
        rabbitmq_message = aio_pika.Message(
            body=message.model_dump_json().encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            **message_kwargs
        )

        # Публикуем сообщение
        await self.exchange.publish(
            message=rabbitmq_message,
            routing_key=routing_key
        )

        logger.debug(f"Message sent to {routing_key}: {message.message_type}")

    async def send_response(self, message: BaseMessage, reply_to: str, correlation_id: str):
        """Отправка ответа во временную очередь"""
        await self._send_message(
            message=message,
            routing_key=reply_to,
            correlation_id=correlation_id
        )
        logger.info(f"Response sent to {reply_to} with correlation_id {correlation_id}")
