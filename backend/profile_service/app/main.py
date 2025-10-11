"""файл запуска сервиса"""#pylint: disable=E0401, E0611, W0621
import sys
import os
from contextlib import asynccontextmanager
from profile_service.messaging.producers import AuthProducer
from profile_service.messaging.consumers import ProfileConsumer
from profile_service.services.service import ProfileService
from profile_service.api.endpoints.profiles import router as profile_router
from fastapi import FastAPI
from shared.database.database import AsyncSessionLocal
from shared.config.base import settings


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

app = FastAPI(
    title="Profile Service",
    description="Service for managing user profiles",
    version="1.0.0"
)

app.include_router(profile_router, prefix="/profiles")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """функция инициализации"""

    auth_producer = AuthProducer(settings.RABBITMQ_URL)
    await auth_producer.connect()

    # Инициализируем и запускаем RabbitMQ consumer
    async with AsyncSessionLocal() as db:
        profile_service = ProfileService(db)
        consumer = ProfileConsumer(settings.RABBITMQ_URL, profile_service)
        await consumer.connect()

        app.state.consumer = consumer

    yield

    await consumer.close()


@app.get("/health")
async def health_check():
    """ручка проверки работоспособности"""
    return {"status": "healthy", "service": "profile"}
