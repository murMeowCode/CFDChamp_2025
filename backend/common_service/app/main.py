"""файл запуска сервиса"""#pylint: disable=E0401, E0611, W0621
import sys
import os
from contextlib import asynccontextmanager

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.utils.redis_client import RedisManager
from shared.messaging.producers import AuthProducer
from shared.database.database import AsyncSessionLocal
from shared.config.base import settings
from profile_service.messaging.consumers import ProfileConsumer
from common_service.services.service import ProfileService
from common_service.api.endpoints.common import router as profile_router
from common_service.services.file_service import FileService
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    """функция инициализации"""

    # Инициализация Redis
    redis_manager = RedisManager()
    cache_client = await redis_manager.get_cache_client()

    try:
        # Пинг Redis для проверки подключения
        ping_result = await cache_client.ping()
        print(f"✅ Redis подключен успешно. Ping: {ping_result}")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        # Можно выбросить исключение или продолжить в зависимости от требований
        raise

    # Инициализация MinIO
    file_service = FileService()
    await file_service.init_minio()

    # Инициализация RabbitMQ producer
    auth_producer = AuthProducer(settings.RABBITMQ_URL)
    await auth_producer.connect()
    print("✅ RabbitMQ producer подключен")

    # Инициализация RabbitMQ consumer
    async with AsyncSessionLocal() as db:
        profile_service = ProfileService(db, file_service)
        consumer = ProfileConsumer(settings.RABBITMQ_URL, profile_service)
        await consumer.connect()
        print("✅ RabbitMQ consumer подключен")

        app.state.consumer = consumer

    yield

    # Завершение работы
    await redis_manager.close_connections()
    print("✅ Redis соединения закрыты")

    await consumer.close()
    print("✅ RabbitMQ consumer отключен")


app = FastAPI(
    title="Profile Service",
    description="Service for managing user profiles",
    lifespan=lifespan
)

app.include_router(profile_router, prefix="/common")

@app.get("/health")
async def health_check():
    """ручка проверки работоспособности"""
    return {"status": "healthy", "service": "profile_service"}
