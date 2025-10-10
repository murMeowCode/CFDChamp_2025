from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime, date
from typing import Optional

class UserCreatedMessage(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    password: str
    role: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime
