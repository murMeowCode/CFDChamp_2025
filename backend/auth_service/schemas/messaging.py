"""схемы для общения с очередями"""
from datetime import date, datetime
import uuid
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr

class MessageType(str, Enum):
    """класс-перечисление типов сообщений"""
    TOKEN_VERIFY_REQUEST = "token.verify.request"
    TOKEN_VERIFY_RESPONSE = "token.verify.response"

    USER_CREATED = "user.created.notification"

class UserCreatedMessage(BaseModel):
    """сообщение о создании пользователя"""
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
    """базовая модель сообщения для отправки в очередь"""
    message_type: MessageType
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

class TokenVerifyMessage(BaseModel):
    """схема токена"""
    token: str

class TokenVerifyResponseMessage(BaseModel):
    """ответ на верификацию"""
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None
    role: int

class TokenRefreshMessage(BaseModel):
    """схема перевыдачи токена в очереди"""
    refresh_token: str

class TokenRefreshResponseMessage(BaseModel):
    """ответ на перевыдачу"""
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    error: Optional[str] = None
