from typing import Any, Dict, List
from fastapi import logger
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
    
    async def get_all_profiles(self) -> List[Profile]:
        result = await self.db.execute(select(Profile))
        return result.scalars().all()
    
    async def update_profile(self, user_id: uuid.UUID, profile_data: ProfileUpdate) -> Profile:
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
            logger.info(f"Profile already exists for user {user_id}")
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
        
        logger.info(f"Profile created for user {user_id}")
        return profile