"""служба работы с профилями"""#pylint: disable=E0401, E0611
from typing import Any, Dict, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.models.profile import Profile
from profile_service.schemas.profile import ProfileUpdate


class ProfileService:
    """класс службы"""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile_by_user_id(self, user_id: uuid.UUID) -> Profile:
        """получение профиля по айди пользователя"""
        result = await self.db.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all_profiles(self) -> List[Profile]:
        """получение всех профилей"""
        result = await self.db.execute(select(Profile))
        return result.scalars().all()

    async def update_profile(self, user_id: uuid.UUID,
                             profile_data: ProfileUpdate) -> Profile:
        """функция обновления профиля"""
        profile = await self.get_profile_by_user_id(user_id)
        if profile:
            update_data = profile_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(profile, field, value)

            await self.db.commit()
            await self.db.refresh(profile)
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
            address=profile_data.get("address")
        )

        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)

        return profile
