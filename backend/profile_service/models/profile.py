"""объявления моделей"""#pylint: disable=E0401, E0611, E1123
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Date, String
from shared.database.database import Base

class Profile(Base):
    """модель профиля"""
    __tablename__ = "profiles"

    user_id = Column(UUID(as_uuid=True),
                      primary_key=True, index=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    birth_date = Column(Date)
    avatar_filename = Column(String(255))
    phone = Column(String(255))
    address = Column(String(255))
