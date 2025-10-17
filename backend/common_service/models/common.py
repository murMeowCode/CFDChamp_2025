"""объявления моделей""" # pylint: disable=E0401
from sqlalchemy import Column, Integer, String

from shared.database.database import Base

class Item(Base):
    """
    Модель общего назначения
    """
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
