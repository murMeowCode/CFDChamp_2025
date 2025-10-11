# auth_service/models/role_change_request.py
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from shared.database.database import Base
import uuid

class RoleChangeRequest(Base):
    __tablename__ = "role_change_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth_users.id"), nullable=False)
    requested_role = Column(Integer, nullable=False)
    current_role = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reason = Column(Text, nullable=True)  # причина запроса
    
    # Relationships
    user = relationship("AuthUser", foreign_keys=[user_id], backref="role_change_requests")
    
    def __repr__(self):
        return f"<RoleChangeRequest {self.user_id} -> {self.requested_role}>"