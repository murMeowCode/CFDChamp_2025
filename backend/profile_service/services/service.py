from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.models.profile import Profile
from profile_service.schemas.profile import ProfileUpdate
from sqlalchemy import select
import uuid

class ProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_profile_by_user_id(self, user_id: uuid.UUID) -> Profile:
        result = await self.db.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_profile(self, user_id: uuid.UUID, profile_data: ProfileUpdate) -> Profile:
        profile = await self.get_profile_by_user_id(user_id)
        if profile:
            update_data = profile_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(profile, field, value)
            
            await self.db.commit()
            await self.db.refresh(profile)
        return profile
    
    async def create_or_update_profile(self, user_id: uuid.UUID, profile_data: ProfileUpdate) -> Profile:
        """Создает или обновляет профиль (если нужно резервное решение)"""
        profile = await self.get_profile_by_user_id(user_id)
        if profile:
            return await self.update_profile(user_id, profile_data)
        else:
            # Если вдруг потребуется создание
            profile = Profile(user_id=user_id, **profile_data.dict(exclude_unset=True))
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
            return profile
