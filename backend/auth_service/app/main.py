import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI
from contextlib import asynccontextmanager
from shared.config.base import settings
from shared.database.database import AsyncSessionLocal
from auth_service.api.endpoints import auth, role_change
from auth_service.services.auth_service import AuthService
from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from auth_service.messaging.producers import AuthProducer
from auth_service.messaging.consumers import AuthConsumer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация RabbitMQ producer
    producer = AuthProducer(settings.RABBITMQ_URL)
    await producer.connect()
    
    # Сохраняем producer в состоянии приложения
    app.state.producer = producer
    
    # Инициализация RabbitMQ consumer
    async with AsyncSessionLocal() as db:
        token_service = TokenService(db)
        user_service = UserService(db)
        auth_service = AuthService(token_service, user_service)
        consumer = AuthConsumer(settings.RABBITMQ_URL, auth_service, producer)
        await consumer.connect()
    
    logger.info("Auth Service started successfully")
    
    yield
    
    # Shutdown
    await producer.close()
    await consumer.close()
    
    logger.info("Auth Service stopped")

app = FastAPI(
    title="Auth Service",
    description="Microservice for JWT token management",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(role_change.router, prefix="/role-change", tags=["role-change"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth_service"}
