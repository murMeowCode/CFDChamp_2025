"""апи для работы с профилями"""#pylint: disable=E0401, E0611
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from shared.utils.auth_utils import get_auth_dependency
from profile_service.services.controller import ProfileController, get_profile_controller
from profile_service.schemas.profile import AvatarUploadResponse, ProfileResponse, ProfileUpdate



router = APIRouter()

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user: dict = Depends(get_auth_dependency().get_current_user),
    controller: ProfileController = Depends(get_profile_controller)
):
    """получение своего профиля"""
    return await controller.get_profile(user["user_id"])

@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    user: dict = Depends(get_auth_dependency().get_current_user),
    controller: ProfileController = Depends(get_profile_controller)
):
    """Эндпоинт для обновления своего профиля"""
    return await controller.update_profile(user["user_id"], profile_data)

@router.post("/me/avatar", response_model=AvatarUploadResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    user: dict = Depends(get_auth_dependency().get_current_user),
    controller: ProfileController = Depends(get_profile_controller)
):
    """Загрузка аватарки пользователя"""
    if not file.filename:
        raise HTTPException(400, "No file provided")

    return await controller.upload_avatar(user["user_id"], file)

@router.get("/all", response_model=List[ProfileResponse])
async def get_all_users(
    _: dict = Depends(lambda: get_auth_dependency().require_role(2)),
    controller: ProfileController = Depends(get_profile_controller)
):
    """Эндпоинт для получения всех пользователей (только для role=2)"""
    return await controller.get_all_profiles()

@router.delete("/avatar", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(
    user: dict = Depends(get_auth_dependency().get_current_user),
    controller: ProfileController = Depends(get_profile_controller)
):
    """Удаление аватарки пользователя"""
    success = await controller.delete_avatar(user["user_id"])
    if not success:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return None
