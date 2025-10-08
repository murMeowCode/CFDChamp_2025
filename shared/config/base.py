from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    
    # База данных
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/auth_service"
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_EXCHANGE: str = "auth_exchange"
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"

settings = Settings()