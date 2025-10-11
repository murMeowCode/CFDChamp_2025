"""апи для работы с профилями"""#pylint: disable=E0401, E0611
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.messaging.producers import AuthProducer
from shared.utils.auth_utils import AuthDependency
from shared.database.database import get_db
from profile_service.services.controller import ProfileController
from profile_service.schemas.profile import ProfileResponse, ProfileUpdate



router = APIRouter()

def get_auth_dependency(producer: AuthProducer = Depends(lambda: AuthDependency.producer)):
    """получение продюсера для проверки прав доступа"""
    return AuthDependency(producer)

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user: dict = Depends(get_auth_dependency().get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """получение своего профиля"""
    controller = ProfileController(db)
    return await controller.get_profile(user["user_id"])

@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    user: dict = Depends(get_auth_dependency().get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Эндпоинт для обновления своего профиля"""
    controller = ProfileController(db)
    return await controller.update_profile(user["user_id"], profile_data)

@router.get("/all", response_model=List[ProfileResponse])
async def get_all_users(
    _: dict = Depends(lambda: get_auth_dependency().require_role(2)),
    db: AsyncSession = Depends(get_db)
):
    """Эндпоинт для получения всех пользователей (только для role=2)"""
    controller = ProfileController(db)
    return await controller.get_all_profiles()
