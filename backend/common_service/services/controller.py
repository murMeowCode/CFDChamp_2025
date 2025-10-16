"""служба взаимодействия с профилем"""#pylint: disable=E0401, E0611
from typing import List
import uuid
from fastapi import HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.services.service import ProfileService
from profile_service.schemas.profile import AvatarUploadResponse, ProfileResponse, ProfileUpdate
from profile_service.services.file_service import FileService, get_file_service
from shared.database.database import get_db


class ProfileController:
    """класс контроллер"""
    def __init__(self, db: AsyncSession, file_service: FileService):
        self.db = db
        self.file_service = file_service
        self.profile_service = ProfileService(db, file_service)

    async def get_profile(self, user_id: uuid.UUID) -> ProfileResponse:
        """получение профиля"""
        profile = await self.profile_service.get_profile_by_user_id(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Обновляем avatar_url если нужно
        if (profile.avatar_filename and
            not profile.avatar_filename.startswith(('http://', 'https://'))):
            profile.avatar_filename = await self.file_service.get_avatar_url(
                profile.avatar_filename)
            await self.profile_service.update_avatar_url(user_id, profile.avatar_filename)

        return ProfileResponse.model_validate(profile)

    async def get_all_profiles(self) -> List[ProfileResponse]:
        """получение всех профилей"""
        profiles = await self.profile_service.get_all_profiles()

        # Обновляем avatar_url для всех профилей
        for profile in profiles:
            if (profile.avatar_filename and
                not profile.avatar_filename.startswith(('http://', 'https://'))):
                profile.avatar_filename = await self.file_service.get_avatar_url(
                    profile.avatar_filename
                    )
                await self.profile_service.update_avatar_url(
                    profile.user_id, profile.avatar_filename)

        return [ProfileResponse.model_validate(profile) for profile in profiles]

    async def update_profile(self, user_id: uuid.UUID,
                             profile_data: ProfileUpdate) -> ProfileResponse:
        """обновление профиля"""
        profile = await self.profile_service.update_profile(user_id, profile_data)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Обновляем avatar_url если нужно
        if (profile.avatar_filename and
            not profile.avatar_filename.startswith(('http://', 'https://'))):
            profile.avatar_filename = await self.file_service.get_avatar_url(
                profile.avatar_filename
                )
            await self.profile_service.update_avatar_url(user_id, profile.avatar_filename)

        return ProfileResponse.model_validate(profile)

    async def upload_avatar(self, user_id: uuid.UUID, file: UploadFile) -> AvatarUploadResponse:
        """Загрузка аватарки пользователя с удалением старой"""
        # Загружаем файл в MinIO (автоматически удаляет старую)
        avatar_url = await self.file_service.upload_avatar(user_id, file)

        # Обновляем профиль с полным URL
        profile = await self.profile_service.update_avatar(user_id, avatar_url)

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        return AvatarUploadResponse(
            avatar_url=avatar_url,
            filename=file.filename
        )

    async def delete_avatar(self, user_id: uuid.UUID) -> bool:
        """Удаление аватарки пользователя"""
        # Удаляем файл из MinIO
        deleted = await self.file_service.delete_avatar(user_id)

        # Обновляем профиль
        if deleted:
            await self.profile_service.update_avatar(user_id, None)

        return deleted

def get_profile_controller(
    db: AsyncSession = Depends(get_db),
    file_service: FileService = Depends(get_file_service)
) -> ProfileController:
    """фабрика контроллеров"""
    return ProfileController(db, file_service)
