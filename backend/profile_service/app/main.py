"""файл запуска сервиса"""#pylint: disable=E0401, E0611, W0621
import sys
import os
from contextlib import asynccontextmanager
from shared.messaging.producers import AuthProducer
from shared.database.database import AsyncSessionLocal
from shared.config.base import settings
from profile_service.messaging.consumers import ProfileConsumer
from profile_service.services.service import ProfileService
from profile_service.api.endpoints.profiles import router as profile_router
from fastapi import FastAPI



sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

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


app = FastAPI(
    title="Profile Service",
    description="Service for managing user profiles",
    lifespan=lifespan
)

app.include_router(profile_router, prefix="/profiles")

@app.get("/health")
async def health_check():
    """ручка проверки работоспособности"""
    return {"status": "healthy", "service": "profile_service"}
