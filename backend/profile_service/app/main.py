from fastapi import FastAPI
from profile_service.api.endpoints.profiles import router as profile_router
from shared.database.database import engine, Base, AsyncSessionLocal
from profile_service.messaging.consumers import ProfileConsumer
from profile_service.services.service import ProfileService
import asyncio
import uvicorn
import os

app = FastAPI(
    title="Profile Service",
    description="Service for managing user profiles",
    version="1.0.0"
)

app.include_router(profile_router, prefix="/api/v1")

# RabbitMQ connection
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

@app.on_event("startup")
async def startup_event():
    # Создаем таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Инициализируем и запускаем RabbitMQ consumer
    async with AsyncSessionLocal() as db:
        profile_service = ProfileService(db)
        consumer = ProfileConsumer(RABBITMQ_URL, profile_service)
        await consumer.connect()
        
        # Сохраняем в app state
        app.state.consumer = consumer

@app.on_event("shutdown")
async def shutdown_event():
    # Закрываем соединения
    if hasattr(app.state, 'consumer'):
        await app.state.consumer.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "profile"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)