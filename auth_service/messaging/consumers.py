import aio_pika
import json
from shared.messaging.base import RabbitMQBase
from auth_service.schemas.messaging import (
    BaseMessage, MessageType, 
    TokenVerifyMessage,
    UserCreatedMessage
)
from auth_service.services.auth_service import AuthService
from auth_service.messaging.producers import AuthProducer

class AuthConsumer(RabbitMQBase):
    def __init__(self, rabbitmq_url: str, auth_service: AuthService, producer: AuthProducer):
        super().__init__(rabbitmq_url)
        self.auth_service = auth_service
        self.producer = producer
        self.queues = {}

    async def connect(self):
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

        # Очереди для событий пользователей
        user_created_queue = await self.channel.declare_queue(
            name="auth.user.created",
            durable=True
        )
        await user_created_queue.bind(exchange, routing_key="user.event.created")
        

        # Начинаем слушать очереди
        await verify_queue.consume(self._handle_verify_request)
        await user_created_queue.consume(self._handle_user_created)

    async def _handle_verify_request(self, message: aio_pika.IncomingMessage):
        """Обработка запроса верификации токена"""
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                base_message = BaseMessage(**body)
                
                if base_message.message_type == MessageType.TOKEN_VERIFY_REQUEST:
                    verify_message = TokenVerifyMessage(**base_message.data)
                    response = await self.auth_service.verify_token_handler(verify_message)
                    
                    # Отправляем ответ
                    response_message = BaseMessage(
                        message_type=MessageType.TOKEN_VERIFY_RESPONSE,
                        data=response.model_dump()
                    )
                    
                    await self.producer.send_response(
                        response_message,
                        base_message.reply_to,
                        base_message.correlation_id
                    )
                    
            except Exception as e:
                print(f"Error processing verify request: {e}")

    async def _handle_user_created(self, message: aio_pika.IncomingMessage):
        """Обработка создания пользователя"""
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                user_data = UserCreatedMessage(**body)
                
                result = await self.auth_service.handle_user_created(user_data)
                if not result["success"]:
                    print(f"Error creating user: {result['error']}")
                    
            except Exception as e:
                print(f"Error processing user created event: {e}")
