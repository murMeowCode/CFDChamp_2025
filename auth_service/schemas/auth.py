from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str
    username: Optional[str] = None

class TokenVerifyRequest(BaseModel):
    token: str

class TokenVerifyResponse(BaseModel):
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    success: bool
    tokens: Optional[TokenPair] = None
    error: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    tokens: Optional[TokenPair] = None
    error: Optional[str] = None