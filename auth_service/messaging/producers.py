import aio_pika
from shared.messaging.base import RabbitMQBase
from auth_service.schemas.messaging import BaseMessage, MessageType, UserCreatedMessage

class AuthProducer(RabbitMQBase):
    def __init__(self, rabbitmq_url: str, exchange_name: str = "auth_exchange"):
        super().__init__(rabbitmq_url)
        self.exchange_name = exchange_name
        self.exchange = None

    async def connect(self):
        await super().connect()
        self.exchange = await self.channel.declare_exchange(
            name=self.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True
        )

    async def send_response(
        self, 
        message: BaseMessage, 
        reply_to: str,
        correlation_id: str
    ):
        """Отправка ответа во временную очередь"""
        if not self.exchange:
            await self.connect()

        response_message = aio_pika.Message(
            body=message.model_dump_json().encode(),
            content_type="application/json",
            correlation_id=correlation_id
        )

        await self.exchange.publish(
            message=response_message,
            routing_key=reply_to
        )

    async def send_user_created_event(self, user_data: UserCreatedMessage):
        """Отправка события создания пользователя"""
        if not self.exchange:
            await self.connect()

        message = BaseMessage(
            message_type=MessageType.USER_CREATED,
            data=user_data.model_dump()
        )

        rabbitmq_message = aio_pika.Message(
            body=message.model_dump_json().encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await self.exchange.publish(
            message=rabbitmq_message,
            routing_key="user.event.created"
        )
