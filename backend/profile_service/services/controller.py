from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.services.service import ProfileService
from profile_service.schemas.profile import ProfileResponse, ProfileUpdate
from shared.database.database import get_db
import uuid

class ProfileController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.profile_service = ProfileService(db)
    
    async def get_profile(self, user_id: uuid.UUID) -> ProfileResponse:
        profile = await self.profile_service.get_profile_by_user_id(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return ProfileResponse.model_validate(profile)
    
    async def get_all_profiles(self) -> List[ProfileResponse]:
        profiles = await self.profile_service.get_all_profiles()
        return [ProfileResponse.model_validate(profile) for profile in profiles]
    
    async def update_profile(self, user_id: uuid.UUID, profile_data: ProfileUpdate) -> ProfileResponse:
        profile = await self.profile_service.update_profile(user_id, profile_data)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return ProfileResponse.model_validate(profile)
