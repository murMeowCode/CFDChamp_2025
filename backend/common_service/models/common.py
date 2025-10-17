"""объявления моделей"""
from sqlalchemy import Column, Integer, String  # pylint: disable=import-error

from shared.database.database import Base  # pylint: disable=import-error


class Item(Base):
    """
    Модель общего назначения
    """
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
