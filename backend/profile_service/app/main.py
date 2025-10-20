"""файл запуска сервиса"""
#pylint: disable=E0401, E0611, W0621, C0413
import sys
import os
from contextlib import asynccontextmanager

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.utils.redis_client import RedisManager
from shared.messaging.producers import AuthProducer
from shared.database.database import AsyncSessionLocal
from shared.config.base import settings
from profile_service.messaging.consumers import ProfileConsumer
from profile_service.services.service import ProfileService
from profile_service.api.endpoints.profiles import router as profile_router
from profile_service.services.file_service import FileService
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    """функция инициализации"""

    # Инициализация компонентов
    redis_manager = RedisManager()
    cache_client = await redis_manager.get_cache_client()
    file_service = FileService()
    auth_producer = AuthProducer(settings.RABBITMQ_URL)

    # Инициализация Redis
    try:
        ping_result = await cache_client.ping()
        print(f"✅ Redis подключен успешно. Ping: {ping_result}")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        raise

    # Инициализация MinIO
    await file_service.init_minio()

    # Инициализация RabbitMQ producer
    await auth_producer.connect()
    print("✅ RabbitMQ producer подключен")

    # Инициализация RabbitMQ consumer
    # Создаем новую сессию для consumer
    db_session = AsyncSessionLocal()
    try:
        profile_service = ProfileService(db_session, file_service)
        consumer = ProfileConsumer(settings.RABBITMQ_URL, profile_service)
        await consumer.connect()
        print("✅ RabbitMQ consumer подключен")

        # Сохраняем компоненты в состоянии приложения
        app.state.redis_manager = redis_manager
        app.state.file_service = file_service
        app.state.auth_producer = auth_producer
        app.state.consumer = consumer
        app.state.db_session = db_session

        yield

    finally:
        # Завершение работы
        await redis_manager.close_connections()
        print("✅ Redis соединения закрыты")

        await consumer.close()
        print("✅ RabbitMQ consumer отключен")

        await auth_producer.close()
        print("✅ RabbitMQ producer отключен")

        await db_session.close()
        print("✅ Database session закрыта")


app = FastAPI(
    title="Profile Service",
    description="Service for managing user profiles",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router, prefix="/profiles")

@app.get("/health")
async def health_check():
    """ручка проверки работоспособности"""
    return {"status": "healthy", "service": "profile_service"}
