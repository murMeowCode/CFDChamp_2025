"""модель аутентифицированного пользователя"""#pylint: disable=E0401
import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from shared.database.database import Base

class AuthUser(Base):
    """модель"""
    __tablename__ = "auth_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(Integer,nullable = False)
    hashed_password = Column(String(255), nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<AuthUser {self.username}>"
