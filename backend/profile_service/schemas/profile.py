"""схемы работы с профилем"""
from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import BaseModel

class ProfileBase(BaseModel):
    """базовая схема профиля"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    avatar_filename: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class ProfileUpdate(ProfileBase):
    """схема обновления профиля"""
    
    class Config:
        # Исключаем поле из схемы
        fields = {
            'avatar_filename': {'exclude': True}
        }

class ProfileResponse(ProfileBase):
    """ответ на действие с профилем"""
    user_id: UUID

    class Config:
        """переход в режим ORM"""
        from_attributes = True

class AvatarUploadResponse(BaseModel):
    """Ответ после загрузки аватарки"""
    avatar_url: str
    filename: str
