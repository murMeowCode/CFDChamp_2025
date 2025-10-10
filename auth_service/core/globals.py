from auth_service.messaging.producers import AuthProducer
from typing import Optional

# Глобальные объекты, инициализированные в lifespan
producer: Optional[AuthProducer] = None

def get_producer() -> AuthProducer:
    """Получение глобального producer"""
    if producer is None:
        raise RuntimeError("Producer not initialized. Application may not be started properly.")
    return producer
