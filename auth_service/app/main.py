from fastapi import FastAPI
from contextlib import asynccontextmanager
from shared.config.base import settings
from shared.database.database import AsyncSessionLocal, get_db, AsyncSession
from api.endpoints import auth
from services.auth_service import AuthService
from services.token_service import TokenService
from services.user_service import UserService
from messaging.producers import AuthProducer
from messaging.consumers import AuthConsumer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = None
consumer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    producer = AuthProducer(settings.RABBITMQ_URL)
    await producer.connect()
    
    async with AsyncSessionLocal() as db:
        token_service = TokenService(db)
        user_service = UserService(db)
        auth_service = AuthService(token_service, user_service)
        consumer = AuthConsumer(settings.RABBITMQ_URL, auth_service, producer)
        await consumer.connect()
    
    yield
    
    await producer.close()
    await consumer.close()

app = FastAPI(
    title="Auth Service",
    description="Microservice for JWT token management",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router,"/auth", tags=["auth"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth_service"}