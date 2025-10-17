"""объявления моделей"""#pylint: disable=E0401, E0611, E1123
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from shared.database.database import Base

class Item(Base):
    """абстрактный класс"""
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
