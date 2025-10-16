"""схемы общения с очередью"""
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    """схема регистрации пользователя"""
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

class UserCreatedMessage(UserRegister):
    """схема получения уведомления о созданном пользователе"""
    user_id: UUID
    created_at: datetime

class MessageType(str, Enum):
    """класс-перечисление типов сообщений"""
    TOKEN_VERIFY_REQUEST = "token_verify_request"
    TOKEN_VERIFY_RESPONSE = "token_verify_response"
    USER_CREATED = "user.created.notification"

class BaseMessage(BaseModel):
    """базовое сообщение из очереди"""
    message_type: MessageType
    data: dict
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

class TokenVerifyMessage(BaseModel):
    """сообщение о верификации токена"""
    token: str

class TokenVerifyResponseMessage(BaseModel):
    """ответ на верификацию"""
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None
    role: Optional[int] = None
