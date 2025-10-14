"""файловая служба для сервиса профилей""" #pylint: disable=E0401
import json
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
    """класс файловой службы"""

    @staticmethod
    async def init_minio():
        """Инициализация MinIO buckets при старте приложения"""
        try:
            # Создаем bucket для аватарок если не существует
            if not minio_client.bucket_exists(settings.MINIO_AVATAR_BUCKET):
                minio_client.make_bucket(settings.MINIO_AVATAR_BUCKET)
                # Устанавливаем политику доступа для публичного чтения
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{settings.MINIO_AVATAR_BUCKET}/*"]
                        }
                    ]
                }
                minio_client.set_bucket_policy(
                    settings.MINIO_AVATAR_BUCKET,
                    json.dumps(policy)
                )
                print(f"""✅ MinIO bucket '{settings.MINIO_AVATAR_BUCKET}'
                       created with public read access""")
            else:
                print(f"✅ MinIO bucket '{settings.MINIO_AVATAR_BUCKET}' already exists")

        except S3Error as e:
            print(f"❌ MinIO initialization error: {e}")
            raise

    @staticmethod
    async def upload_avatar(user_id: uuid.UUID, file: UploadFile) -> str:
        """Загрузка аватарки пользователя с удалением старой"""
        # Генерируем уникальное имя файла
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{user_id}/avatar.{file_extension}"  # Постоянное имя для каждого пользователя

        # Проверяем тип файла
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "Only image files are allowed")

        try:
            # Удаляем старую аватарку если существует
            await FileService.delete_avatar(user_id)

            # Загружаем новую аватарку
            contents = await file.read()
            minio_client.put_object(
                bucket_name=settings.MINIO_AVATAR_BUCKET,
                object_name=filename,
                data=BytesIO(contents),
                length=len(contents),
                content_type=file.content_type
            )

            # Генерируем публичный URL для фронта
            avatar_url = await FileService.get_avatar_url(filename)
            return avatar_url

        except S3Error as e:
            raise HTTPException(500, f"Upload failed: {str(e)}")

    @staticmethod
    async def delete_avatar(user_id: uuid.UUID) -> bool:
        """Удаление аватарки пользователя"""
        try:
            # Ищем все файлы в папке пользователя
            objects = minio_client.list_objects(
                settings.MINIO_AVATAR_BUCKET, 
                prefix=f"{user_id}/"
            )

            deleted = False
            for obj in objects:
                minio_client.remove_object(settings.MINIO_AVATAR_BUCKET, obj.object_name)
                deleted = True
                print(f"🗑️ Deleted old avatar: {obj.object_name}")

            return deleted
        except S3Error as e:
            print(f"⚠️ Error deleting old avatar: {e}")
            return False

    @staticmethod
    async def get_avatar_url(filename: str) -> str:
        """Получение публичного URL аватарки"""
        if not filename:
            return None

        try:
            # Для MinIO с настройкой public access можно использовать прямой URL
            if settings.MINIO_SECURE:
                return f"""https://{settings.MINIO_ENDPOINT}/
                    {settings.MINIO_AVATAR_BUCKET}/{filename}"""
            
            return f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_AVATAR_BUCKET}/{filename}"
        except Exception as e:
            print(f"⚠️ Error generating avatar URL: {e}")
            return None

    @staticmethod
    async def get_user_avatar_url(user_id: uuid.UUID) -> str:
        """Получение URL аватарки пользователя по user_id"""
        try:
            # Ищем аватарку пользователя
            objects = minio_client.list_objects(
                settings.MINIO_AVATAR_BUCKET, 
                prefix=f"{user_id}/"
            )

            for obj in objects:
                if obj.object_name.startswith(f"{user_id}/avatar."):
                    return await FileService.get_avatar_url(obj.object_name)
            
            return None
        except S3Error:
            return None

async def get_file_service() -> FileService:
    """генератор службы"""
    file_service = FileService()
    return file_service
