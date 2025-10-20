"""служба работы с профилями"""#pylint: disable=E0401, E0611
from typing import Any, Dict, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.models.profile import Profile
from profile_service.schemas.profile import ProfileUpdate
from profile_service.services.file_service import FileService


class ProfileService:
    """класс службы"""    
    def __init__(self, db: AsyncSession, file_service: FileService):
        self.db = db
        self.file_service = file_service

    async def update_avatar(self, user_id: uuid.UUID, avatar_url: str) -> Profile:
        """Обновление аватарки в профиле"""
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            return None

        profile.avatar_filename = avatar_url
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def update_avatar_url(self, user_id: uuid.UUID, avatar_url: str) -> None:
        """Обновление только URL аватарки"""
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        if profile:
            profile.avatar_filename = avatar_url
            await self.db.commit()

    async def get_profile_by_user_id(self, user_id: uuid.UUID) -> Profile:
        """получение профиля по айди пользователя"""
        result = await self.db.execute(
            select(Profile).where(Profile.user_id == user_id)
        )

        profile = result.scalar_one_or_none()

        if profile and profile.avatar_filename:
            profile.avatar_filename = await self.file_service.get_avatar_url(
                profile.avatar_filename)

        return profile

    async def get_all_profiles(self) -> List[Profile]:
        """получение всех профилей"""
        result = await self.db.execute(select(Profile))

        profiles = result.scalars().all()

        for profile in profiles:
            if profile.avatar_filename:
                profile.avatar_filename = await self.file_service.get_avatar_url(
                    profile.avatar_filename)

        return profiles

    async def update_profile(self, user_id: uuid.UUID, profile_data: ProfileUpdate) -> Profile:
        """функция обновления профиля"""
        profile = await self.get_profile_by_user_id(user_id)
        if profile:
            update_data = profile_data.dict(exclude_unset=True, exclude={'avatar_url'})
            for field, value in update_data.items():
                setattr(profile, field, value)

            await self.db.commit()
            await self.db.refresh(profile)

            # Обновляем URL аватарки
            if profile.avatar_filename:
                profile.avatar_filename = await self.file_service.get_avatar_url(
                    profile.avatar_filename)

        return profile


    async def create_profile_from_message(self, profile_data: Dict[str, Any]) -> Profile:
        """Создает профиль из данных сообщения"""
        user_id = profile_data["user_id"]

        # Проверяем, не существует ли уже профиль
        existing_profile = await self.get_profile_by_user_id(user_id)
        if existing_profile:
            return existing_profile

        # Создаем новый профиль
        profile = Profile(
            user_id=user_id,
            first_name=profile_data.get("first_name"),
            last_name=profile_data.get("last_name"),
            middle_name=profile_data.get("middle_name"),
            birth_date=profile_data.get("birth_date"),
            phone=profile_data.get("phone"),
            address=profile_data.get("address"),
            avatar_filename=profile_data.get("avatar_url")
        )

        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)

        return profile
