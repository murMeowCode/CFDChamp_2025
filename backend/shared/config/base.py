"""общие настройки сервисов"""#pylint: disable=R0903
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """класс настроек"""

    # База данных
    DATABASE_URL: str = "postgresql+asyncpg://test:test@127.0.0.1:5432/postgres"
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_EXCHANGE: str = "auth_exchange"
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    #Email
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str = "onboarding@resend.dev"
    #MinIO
    MINIO_ENDPOINT = "localhost:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE : bool = False
    MINIO_AVATAR_BUCKET: str = "avatars"

    class Config:
        """импорт из файла среды"""
        env_file = ".env"

settings = Settings()
