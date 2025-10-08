from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from shared.database.database import Base

class AuthUser(Base):
    __tablename__ = "auth_users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<AuthUser {self.username}>"