"""основной модуль сервиса""" #pylint: disable=E0401, C0413, W0718, W1203
import asyncio
from contextlib import asynccontextmanager
import logging
import os
import sys
from fastapi import FastAPI

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


from mailing_service.api.endpoints.message import router as mailing_router
from mailing_service.messaging.consumers import MailingConsumer
from shared.config.base import settings
from shared.messaging.producers import AuthProducer

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    """функция инициализации"""
    
    print("🚀 Starting lifespan...")
    
    auth_producer = AuthProducer(settings.RABBITMQ_URL)
    await auth_producer.connect()
    print("✅ RabbitMQ producer подключен")

    mail_consumer = MailingConsumer(rabbitmq_url=settings.RABBITMQ_URL)
    try:
        print("🔄 Connecting consumer...")
        await mail_consumer.connect()
        print("✅ RabbitMQ consumer подключен")
        
        # Проверяем состояние канала
        print(f"📡 Channel is open: {not mail_consumer.channel.is_closed}")
        print(f"📡 Exchange name: {mail_consumer.exchange_name}")
        
        print("🔄 Setting up queues...")
        print("✅ Queues setup completed")
        
        # Проверим, что consumer действительно слушает
        await asyncio.sleep(1)  # Даем время на установку
        print("🎯 Consumer should be listening now...")
        
    except Exception as e:
        print(f"❌ Failed during consumer setup: {e}")
        import traceback
        traceback.print_exc()
        raise

    yield

    print("🛑 Shutting down...")
    await mail_consumer.close()
    print("✅ Consumer closed")

app = FastAPI(title="Mailing Service",lifespan=lifespan)
app.include_router(mailing_router)

@app.get("/health")
async def health_check():
    """апи для проверки работоспособности сервиса"""
    return {"status": "healthy", "service": "mailing_service"}
