from fastapi import FastAPI
from contextlib import asynccontextmanager
from shared.config.base import settings
from shared.database.database import init_db, get_db
from api.endpoints import auth
from services.auth_service import AuthService
from services.token_service import TokenService
from messaging.producers import AuthProducer
from messaging.consumers import AuthConsumer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = None
consumer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    
    # Инициализация RabbitMQ
    global producer, consumer
    
    producer = AuthProducer(settings.RABBITMQ_URL)
    await producer.connect()
    
    async for db in get_db():
        token_service = TokenService(db)
        auth_service = AuthService(token_service)
        consumer = AuthConsumer(settings.RABBITMQ_URL, auth_service, producer)
        await consumer.connect()
        break
    
    logger.info("Auth Service started successfully")
    
    yield
    
    # Shutdown
    if producer:
        await producer.close()
    if consumer:
        await consumer.close()
    
    logger.info("Auth Service stopped")

app = FastAPI(
    title="Auth Service",
    description="Microservice for JWT token management",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth_service"}