from datetime import date, datetime
import uuid
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserRegister(BaseModel):
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

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserRegisterResponse(BaseModel):
    success: bool
    user_id: Optional[uuid.UUID] = None
    error: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    role: int
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

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

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    role: str
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
