from datetime import date, datetime
import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from enum import Enum

class MessageType(str, Enum):
    TOKEN_VERIFY_REQUEST = "token.verify.request"
    TOKEN_VERIFY_RESPONSE = "token.verify.response"

    USER_CREATED = "user.created.notification"

class UserCreatedMessage(BaseModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr
    password: str
    role: int
    # Дополнительная информация для основного сервиса
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime

class BaseMessage(BaseModel):
    message_type: MessageType
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

class TokenVerifyMessage(BaseModel):
    token: str

class TokenVerifyResponseMessage(BaseModel):
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None

class TokenRefreshMessage(BaseModel):
    refresh_token: str

class TokenRefreshResponseMessage(BaseModel):
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    error: Optional[str] = None

# User event messages
class UserCreatedMessage(BaseModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr
    password: str  # Пароль в открытом виде для хеширования
    created_at: datetime
    role: int
