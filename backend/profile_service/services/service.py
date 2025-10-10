from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.models.profile import Profile


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def get_profile_by_user_id(self, user_id: int) -> Profile:
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()
    
    def update_profile(self, user_id: int, profile_data: ProfileUpdate) -> Profile:
        profile = self.get_profile_by_user_id(user_id)
        if profile:
            for field, value in profile_data.dict(exclude_unset=True):
                setattr(profile, field, value)
            self.db.commit()
            self.db.refresh(profile)
        return profile
