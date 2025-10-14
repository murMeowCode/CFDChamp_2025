"""Служба работы с файлами"""
import uuid
from datetime import timedelta
from io import BytesIO
from minio.error import S3Error
from fastapi import HTTPException, UploadFile
from shared.config.minio import minio_client
from shared.config.base import settings

class FileService:
    """Сервис для работы с файлами в MinIO"""

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
            # Читаем файл в память
            contents = await file.read()

            # Загружаем в MinIO
            minio_client.put_object(
                bucket_name=settings.MINIO_AVATAR_BUCKET,
                object_name=filename,
                data=BytesIO(contents),
                length=len(contents),
                content_type=file.content_type
            )

            return filename

        except S3Error as e:
            raise HTTPException(500, f"Failed to upload avatar: {str(e)}")
        except Exception as e:
            raise HTTPException(500, f"Upload error: {str(e)}")

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

    @staticmethod
    async def delete_avatar(filename: str):
        """Удаление аватарки"""
        if not filename:
            return

        try:
            minio_client.remove_object(settings.MINIO_AVATAR_BUCKET, filename)
        except S3Error:
            pass  # Логируем, но не падаем

file_service = FileService()
