# auth_service/api/role_change.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from auth_service.models.user import AuthUser
from shared.database.database import get_db
from auth_service.services.role_change_service import RoleChangeService
from auth_service.services.user_service import UserService
from auth_service.schemas.role_change import (
    RoleChangeRequestCreate, 
    RoleChangeRequestResponse, 
    RoleChangeRequestList
)
from auth_service.core.auth import get_current_user

router = APIRouter(prefix="/role-change", tags=["role-change"])

@router.post("/request", status_code=status.HTTP_201_CREATED)
async def create_role_change_request(
    request_data: RoleChangeRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Создание заявки на изменение роли"""
    role_change_service = RoleChangeService(db)
    
    try:
        request = await role_change_service.create_role_change_request(current_user.id, request_data)
        
        # Получаем username для ответа
        user_service = UserService(db)
        user = await user_service.get_user_by_id(current_user.id)
        
        return RoleChangeRequestResponse(
            id=request.id,
            user_id=request.user_id,
            current_role=request.current_role,
            requested_role=request.requested_role,
            status=request.status,
            reason=request.reason,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/requests", response_model=RoleChangeRequestList)
async def get_pending_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Получение списка pending заявок (только для пользователей с достаточными правами)"""
    # Здесь можно добавить проверку прав доступа
    # if current_user.role < REQUIRED_ROLE_FOR_REVIEW:
    #     raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    role_change_service = RoleChangeService(db)
    user_service = UserService(db)
    
    requests = await role_change_service.get_pending_requests(skip, limit)
    
    # Формируем ответ с username'ами
    response_requests = []
    for req in requests:
        user = await user_service.get_user_by_id(req.user_id)
        reviewer_username = None
        if req.reviewed_by:
            reviewer = await user_service.get_user_by_id(req.reviewed_by)
            reviewer_username = reviewer.username if reviewer else None
        
        response_requests.append(RoleChangeRequestResponse(
            id=req.id,
            user_id=req.user_id,
            current_role=req.current_role,
            requested_role=req.requested_role,
            status=req.status,
            reason=req.reason,
        ))
    
    return RoleChangeRequestList(
        requests=response_requests,
        total=len(response_requests)
    )

@router.post("/{request_id}/approve")
async def approve_role_change_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Одобрение заявки на изменение роли"""
    role_change_service = RoleChangeService(db)
    
    result = await role_change_service.approve_request(request_id, current_user.id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return {"success": True, "message": result["message"]}

@router.post("/{request_id}/reject")
async def reject_role_change_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user)
):
    """Отклонение заявки на изменение роли"""
    role_change_service = RoleChangeService(db)
    
    result = await role_change_service.reject_request(request_id, current_user.id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return {"success": True, "message": result["message"]}
