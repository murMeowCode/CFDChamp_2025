import aio_pika
import json
from shared.messaging.base import RabbitMQBase
from schemas.messaging import (
    BaseMessage, MessageType, 
    TokenVerifyMessage, TokenRefreshMessage,
    TokenVerifyResponseMessage, TokenRefreshResponseMessage
)
from services.auth_service import AuthService
from messaging.producers import AuthProducer

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

        # Очередь для верификации токенов
        verify_queue = await self.channel.declare_queue(
            name="auth.verify.request",
            durable=True
        )
        await verify_queue.bind(exchange, routing_key="auth.verify.request")
        
        # Очередь для обновления токенов
        refresh_queue = await self.channel.declare_queue(
            name="auth.refresh.request", 
            durable=True
        )
        await refresh_queue.bind(exchange, routing_key="auth.refresh.request")

        # Начинаем слушать очереди
        await verify_queue.consume(self._handle_verify_request)
        await refresh_queue.consume(self._handle_refresh_request)

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

    async def _handle_refresh_request(self, message: aio_pika.IncomingMessage):
        """Обработка запроса обновления токенов"""
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                base_message = BaseMessage(**body)
                
                if base_message.message_type == MessageType.TOKEN_REFRESH_REQUEST:
                    refresh_message = TokenRefreshMessage(**base_message.data)
                    response = await self.auth_service.refresh_token_handler(refresh_message)
                    
                    # Отправляем ответ
                    response_message = BaseMessage(
                        message_type=MessageType.TOKEN_REFRESH_RESPONSE,
                        data=response.model_dump()
                    )
                    
                    await self.producer.send_response(
                        response_message,
                        base_message.reply_to,
                        base_message.correlation_id
                    )
                    
            except Exception as e:
                print(f"Error processing refresh request: {e}")