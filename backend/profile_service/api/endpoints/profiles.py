from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from profile_service.services.controller import ProfileController
from profile_service.schemas.profile import ProfileResponse, ProfileUpdate
from shared.database.database import get_db
import uuid
from typing import List

router = APIRouter()

# Новый эндпоинт /me для текущего пользователя
@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user_id: uuid.UUID,  # Будем получать из JWT токена или заголовков
    db: AsyncSession = Depends(get_db)
):
    controller = ProfileController(db)
    return await controller.get_profile(user_id)

@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    user_id: uuid.UUID,  # Будем получать из JWT токена или заголовков
    profile_data: ProfileUpdate,
    db: AsyncSession = Depends(get_db)
):
    controller = ProfileController(db)
    return await controller.update_profile(user_id, profile_data)

# Эндпоинт для получения всех пользователей
@router.get("/users", response_model=List[ProfileResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db)
):
    controller = ProfileController(db)
    return await controller.get_all_profiles()
