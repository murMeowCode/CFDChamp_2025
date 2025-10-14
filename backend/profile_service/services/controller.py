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
    """класс-контроллер"""
    def __init__(self, db: AsyncSession = Depends(get_db),
                 file_service: FileService = Depends(get_file_service)):
        self.db = db
        self.file_service = file_service
        self.profile_service = ProfileService(db,file_service)

    async def get_profile(self, user_id: uuid.UUID) -> ProfileResponse:
        """получение профиля"""
        profile = await self.profile_service.get_profile_by_user_id(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return ProfileResponse.model_validate(profile)

    async def get_all_profiles(self) -> List[ProfileResponse]:
        """получение всех профилей"""
        profiles = await self.profile_service.get_all_profiles()
        return [ProfileResponse.model_validate(profile) for profile in profiles]

    async def update_profile(self, user_id: uuid.UUID,
                             profile_data: ProfileUpdate) -> ProfileResponse:
        """обновление профиля"""
        profile = await self.profile_service.update_profile(user_id, profile_data)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return ProfileResponse.model_validate(profile)

    async def upload_avatar(self, user_id: uuid.UUID, file: UploadFile) -> AvatarUploadResponse:
        """Загрузка аватарки пользователя"""
        # Загружаем файл в MinIO
        filename = await self.file_service.upload_avatar(user_id, file)

        # Обновляем профиль
        profile = await self.profile_service.update_avatar(user_id, filename)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        return AvatarUploadResponse(
            avatar_url=profile.avatar_filename,
            filename=filename
        )
