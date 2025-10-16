"""объявления моделей"""#pylint: disable=E0401, E0611, E1123
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Date, String, Integer
from shared.database.database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)