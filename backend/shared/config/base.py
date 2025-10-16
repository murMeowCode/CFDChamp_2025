"""общие настройки сервисов"""#pylint: disable=R0903
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """класс настроек"""

    # База данных
    DATABASE_URL: str = "postgresql+asyncpg://postgres:slon_311.@212.111.87.142:5666/postgres"
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@212.111.87.142:5672/"
    RABBITMQ_EXCHANGE: str = "auth_exchange"
    # JWT
    JWT_SECRET_KEY: str = "RAhuvd1qzpdKcjeYsAoIQxKeRKaa-pBJb9iksJ9DAWQ"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    #Email
    RESEND_API_KEY: str = "re_PNUDqH1W_prku9ViR4NwVZs2TeDsmDUst"
    RESEND_FROM_EMAIL: str = "onboarding@resend.dev"
    #MinIO
    MINIO_ENDPOINT: str = "212.111.87.142:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minio_311."
    MINIO_SECURE : bool = False
    MINIO_AVATAR_BUCKET: str = "avatars"

    # Redis
    REDIS_HOST="212.111.87.142"
    REDIS_PORT=6379
    REDIS_DB_CACHE=0
    REDIS_DB_CELERY=1
    REDIS_PASSWORD="redis_311."

    class Config:
        """импорт из файла среды"""
        env_file = ".env"

settings = Settings()
