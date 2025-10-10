from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core.globals import get_producer
from auth_service.services.registration_service import RegistrationService
from shared.database.database import get_db
from schemas.auth import (LoginRequest, LoginResponse, RefreshTokenRequest,
                          RefreshTokenResponse, UserRegister, UserRegisterResponse, UserResponse)
from services.token_service import TokenService
from services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
    producer = Depends(get_producer)  # Используем глобальный producer
):
    """Регистрация нового пользователя"""
    registration_service = RegistrationService(db, producer)
    result = await registration_service.register_user(user_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return UserRegisterResponse(
        success=True,
        user_id=result["user_id"]
    )

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Аутентификация пользователя"""
    user_service = UserService(db)
    token_service = TokenService(db)
    
    # Аутентифицируем пользователя
    user = await user_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Обновляем время последнего входа
    await user_service.update_user_last_login(user.id)
    
    # Создаем токены
    tokens = await token_service.create_token_pair(
        user_id=str(user.id),
        username=user.username
    )
    
    user_response = UserResponse.from_orm(user)
    
    return LoginResponse(
        success=True,
        tokens=tokens,
        user=user_response
    )

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_tokens(refresh_data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Обновление пары токенов"""
    token_service = TokenService(db)
    result = await token_service.refresh_tokens(refresh_data.refresh_token)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return RefreshTokenResponse(
        success=True,
        tokens=result["tokens"]
    )

@router.post("/verify")
async def verify_token(token: str, db: AsyncSession = Depends(get_db)):
    """Прямая верификация токена (для тестирования)"""
    token_service = TokenService(db)
    result = await token_service.verify_access_token(token)
    
    if not result["valid"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"]
        )
    
    return result
