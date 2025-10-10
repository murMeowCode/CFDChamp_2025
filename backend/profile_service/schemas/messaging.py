from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from enum import Enum

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

class MessageType(str, Enum):
    TOKEN_VERIFY_REQUEST = "token_verify_request"
    TOKEN_VERIFY_RESPONSE = "token_verify_response"

class BaseMessage(BaseModel):
    message_type: MessageType
    data: dict
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

class TokenVerifyMessage(BaseModel):
    token: str

class TokenVerifyResponseMessage(BaseModel):
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None
    role: Optional[int] = None