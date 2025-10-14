"""файловая служба для аватарок"""
from datetime import timedelta
import uuid
from io import BytesIO
from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException, UploadFile
from shared.config.base import settings

# Клиент создается здесь, а не в shared
minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY, 
    secure=settings.MINIO_SECURE
)

class FileService:
    @staticmethod
    async def upload_avatar(user_id: uuid.UUID, file: UploadFile) -> str:
        # Используем локальный minio_client
        filename = f"{user_id}/avatar_{uuid.uuid4()}.jpg"

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
    async def get_avatar_url(filename: str, expires_hours: int = 24) -> str:
        """Генерация временной ссылки на аватарку"""
        if not filename:
            return None

        try:
            return minio_client.presigned_get_object(
                bucket_name=settings.MINIO_AVATAR_BUCKET,
                object_name=filename,
                expires=timedelta(hours=expires_hours)
            )
        except S3Error:
            return None

# Создаем инстанс сервиса
file_service = FileService()