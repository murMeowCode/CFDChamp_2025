from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    user_id: UUID
    
    class Config:
        from_attributes = True