"""основной модуль сервиса""" #pylint: disable=E0401
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from mailing_service.api.endpoints.message import router as mailing_router
from mailing_service.messaging.consumers import MailingConsumer
from shared.config.base import settings
from shared.messaging.producers import AuthProducer

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    """функция инициализации"""

    auth_producer = AuthProducer(settings.RABBITMQ_URL)
    await auth_producer.connect()

    mail_consumer = MailingConsumer(rabbitmq_url=settings.RABBITMQ_URL)
    try:
        await mail_consumer.connect()
        logger.info("Successfully connected to RabbitMQ")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")

    yield

    await mail_consumer.close()

app = FastAPI(title="CFDChamp API",lifespan=lifespan)
app.include_router(mailing_router)

@app.get("/health")
async def health_check():
    """апи для проверки работоспособности сервиса"""
    return {"status": "healthy", "service": "mailing_service"}
