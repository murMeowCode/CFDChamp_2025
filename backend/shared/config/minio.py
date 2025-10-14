"""конфиг файл для MinIO"""
from minio import Minio
from shared.config.base import settings

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,  # "minio:9000" или "localhost:9000"
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE  # False для разработки
)

async def init_minio():
    """Инициализация MinIO при старте приложения"""
    try:
        if not minio_client.bucket_exists("avatars"):
            minio_client.make_bucket("avatars")
        print("✅ MinIO buckets initialized")
    except Exception as e:
        print(f"❌ MinIO init error: {e}")
