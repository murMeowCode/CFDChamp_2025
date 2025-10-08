from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class MessageType(str, Enum):
    TOKEN_VERIFY_REQUEST = "token.verify.request"
    TOKEN_VERIFY_RESPONSE = "token.verify.response"
    TOKEN_REFRESH_REQUEST = "token.refresh.request"
    TOKEN_REFRESH_RESPONSE = "token.refresh.response"

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