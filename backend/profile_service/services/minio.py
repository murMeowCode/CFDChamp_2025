"""инициализация клиента для профиля"""
from minio import Minio
from shared.config.base import settings

# Создаем клиент MinIO
minio_client_profile = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

async def init_minio_for_profile():
    """Инициализация buckets для профиль-сервиса"""
    try:
        if not minio_client_profile.bucket_exists("avatars"):
            minio_client_profile.make_bucket("avatars")
        print("✅ ProfileService: MinIO buckets initialized")
    except Exception as e:
        print(f"❌ ProfileService MinIO init error: {e}")