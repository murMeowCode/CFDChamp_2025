# auth_service/schemas/role_change.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class RoleChangeStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class RoleChangeRequestCreate(BaseModel):
    requested_role: int
    reason: Optional[str] = None

class RoleChangeRequestResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    username: str
    current_role: int
    requested_role: int
    status: RoleChangeStatus
    reason: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]
    reviewed_by: Optional[uuid.UUID]
    reviewer_username: Optional[str]
    
    class Config:
        from_attributes = True

class RoleChangeRequestUpdate(BaseModel):
    status: RoleChangeStatus

class RoleChangeRequestList(BaseModel):
    requests: list[RoleChangeRequestResponse]
    total: int