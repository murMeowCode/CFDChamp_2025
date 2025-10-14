"""файловая служба для сервиса профилей""" #pylint: disable=E0401
import uuid
from io import BytesIO
from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException, UploadFile
from shared.config.base import settings

# Клиент создается здесь
minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY, 
    secure=settings.MINIO_SECURE
)

class FileService:

    @staticmethod
    async def init_minio():
        """Инициализация MinIO buckets при старте приложения"""
        try:
            # Создаем bucket для аватарок если не существует
            if not minio_client.bucket_exists(settings.MINIO_AVATAR_BUCKET):
                minio_client.make_bucket(settings.MINIO_AVATAR_BUCKET)
                print(f"✅ MinIO bucket '{settings.MINIO_AVATAR_BUCKET}' created")
            else:
                print(f"✅ MinIO bucket '{settings.MINIO_AVATAR_BUCKET}' already exists")
                
        except S3Error as e:
            print(f"❌ MinIO initialization error: {e}")
            raise

    @staticmethod
    async def upload_avatar(user_id: uuid.UUID, file: UploadFile) -> str:
        """Загрузка аватарки пользователя"""
        # Генерируем уникальное имя файла
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{user_id}/avatar_{uuid.uuid4()}.{file_extension}"

        # Проверяем тип файла
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "Only image files are allowed")

        try:
            contents = await file.read()
            minio_client.put_object(
                bucket_name=settings.MINIO_AVATAR_BUCKET,
                object_name=filename,
                data=BytesIO(contents),
                length=len(contents),
                content_type=file.content_type
            )
            return filename
        except S3Error as e:
            raise HTTPException(500, f"Upload failed: {str(e)}")

    @staticmethod
    async def get_avatar_url(filename: str) -> str:
        """Получение URL аватарки"""
        if not filename:
            return None
        try:
            return minio_client.presigned_get_object(
                bucket_name=settings.MINIO_AVATAR_BUCKET,
                object_name=filename
            )
        except S3Error:
            return None
