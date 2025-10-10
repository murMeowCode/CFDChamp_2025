import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from profile_service.api.endpoints.profiles import router as profile_router
from shared.database.database import AsyncSessionLocal
from profile_service.messaging.consumers import ProfileConsumer
from profile_service.services.service import ProfileService
from shared.config.base import settings
import uvicorn

app = FastAPI(
    title="Profile Service",
    description="Service for managing user profiles",
    version="1.0.0"
)

app.include_router(profile_router, prefix="/api/v1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    
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
    return {"status": "healthy", "service": "profile"}
