from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.messaging.producers import AuthProducer
from profile_service.services.auth import AuthDependency
from profile_service.services.controller import ProfileController
from profile_service.schemas.profile import ProfileResponse, ProfileUpdate
from shared.database.database import get_db
import uuid
from typing import List

router = APIRouter()

def get_auth_dependency(producer: AuthProducer = Depends(lambda: AuthDependency.producer)):
    return AuthDependency(producer)

# Эндпоинт для получения своего профиля
@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user: dict = Depends(get_auth_dependency().get_current_user),
    db: AsyncSession = Depends(get_db)
):
    controller = ProfileController(db)
    return await controller.get_profile(user["user_id"])

# Эндпоинт для обновления своего профиля
@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    user: dict = Depends(get_auth_dependency().get_current_user),
    db: AsyncSession = Depends(get_db)
):
    controller = ProfileController(db)
    return await controller.update_profile(user["user_id"], profile_data)

# Эндпоинт для получения всех пользователей (только для role=2)
@router.get("/all", response_model=List[ProfileResponse])
async def get_all_users(
    user: dict = Depends(lambda: get_auth_dependency().require_role(2)),
    db: AsyncSession = Depends(get_db)
):
    controller = ProfileController(db)
    return await controller.get_all_profiles()
