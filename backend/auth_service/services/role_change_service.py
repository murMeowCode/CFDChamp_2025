# auth_service/services/role_change_service.py
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import uuid

from auth_service.models.user import AuthUser
from auth_service.models.role_change_request import RoleChangeRequest
from auth_service.schemas.role_change import RoleChangeRequestCreate, RoleChangeStatus

class RoleChangeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_role_change_request(self, user_id: uuid.UUID, request_data: RoleChangeRequestCreate) -> RoleChangeRequest:
        """Создание заявки на изменение роли"""
        # Получаем пользователя
        user = await self.db.get(AuthUser, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Проверяем, что запрашиваемая роль отличается от текущей
        if user.role == request_data.requested_role:
            raise ValueError("Requested role is the same as current role")
        
        # Проверяем, есть ли уже pending заявка у пользователя
        existing_pending_stmt = select(RoleChangeRequest).where(
            and_(
                RoleChangeRequest.user_id == user_id,
                RoleChangeRequest.status == RoleChangeStatus.PENDING
            )
        )
        existing_pending = await self.db.execute(existing_pending_stmt)
        if existing_pending.scalar_one_or_none():
            raise ValueError("User already has a pending role change request")
        
        # Создаем заявку
        role_request = RoleChangeRequest(
            user_id=user_id,
            current_role=user.role,
            requested_role=request_data.requested_role,
            reason=request_data.reason,
            status=RoleChangeStatus.PENDING
        )
        
        self.db.add(role_request)
        await self.db.commit()
        await self.db.refresh(role_request)
        
        return role_request

    async def get_pending_requests(self, skip: int = 0, limit: int = 100) -> List[RoleChangeRequest]:
        """Получение списка pending заявок"""
        stmt = select(RoleChangeRequest).where(
            RoleChangeRequest.status == RoleChangeStatus.PENDING
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_request_by_id(self, request_id: uuid.UUID) -> Optional[RoleChangeRequest]:
        """Получение заявки по ID"""
        return await self.db.get(RoleChangeRequest, request_id)

    async def get_user_requests(self, user_id: uuid.UUID) -> List[RoleChangeRequest]:
        """Получение заявок пользователя"""
        stmt = select(RoleChangeRequest).where(
            RoleChangeRequest.user_id == user_id
        ).order_by(RoleChangeRequest.created_at.desc())
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def approve_request(self, request_id: uuid.UUID) -> Dict:
        """Одобрение заявки на изменение роли"""
        role_request = await self.get_request_by_id(request_id)
        if not role_request:
            return {"success": False, "error": "Request not found"}
        
        if role_request.status != RoleChangeStatus.PENDING:
            return {"success": False, "error": "Request is not pending"}
        
        # Получаем пользователя
        user = await self.db.get(AuthUser, role_request.user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        # Обновляем роль пользователя
        user.role = role_request.requested_role
        
        # Обновляем заявку
        role_request.status = RoleChangeStatus.APPROVED
        
        await self.db.commit()
        
        return {
            "success": True, 
            "message": f"Role changed from {role_request.current_role} to {role_request.requested_role}"
        }

    async def reject_request(self, request_id: uuid.UUID) -> Dict:
        """Отклонение заявки на изменение роли"""
        role_request = await self.get_request_by_id(request_id)
        if not role_request:
            return {"success": False, "error": "Request not found"}
        
        if role_request.status != RoleChangeStatus.PENDING:
            return {"success": False, "error": "Request is not pending"}
        
        # Обновляем заявку
        role_request.status = RoleChangeStatus.REJECTED
        
        await self.db.commit()
        
        return {"success": True, "message": "Request rejected"}
