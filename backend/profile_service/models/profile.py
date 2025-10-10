from datetime import date
from sqlalchemy import Column, String
from shared.database.database import Base
import uuid

class Profile(Base):
    __tablename__ = "profiles"
    
    user_id = Column(uuid.UUID(as_uuid=True), primary_key=True, index=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    brith_date = date
    avatar_url = Column(String(255))
    phone = Column(String(255))
    address = Column(String(255))
