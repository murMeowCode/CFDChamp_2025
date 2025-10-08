from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.database import get_db
from schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from services.token_service import TokenService

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Эндпоинт для логина (заглушка - в реальности проверяем с user_service)"""
    # TODO: Интеграция с user_service для проверки учетных данных
    # Пока заглушка - всегда успешный логин для тестирования
    
    token_service = TokenService(db)
    tokens = await token_service.create_token_pair(
        user_id="123e4567-e89b-12d3-a456-426614174000",  # Заглушка
        username=login_data.username
    )
    
    return LoginResponse(
        success=True,
        tokens=tokens
    )

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_tokens(refresh_data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Обновление пары токенов"""
    token_service = TokenService(db)
    result = await token_service.refresh_tokens(refresh_data.refresh_token)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
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
        raise HTTPException(status_code=401, detail=result["error"])
    
    return result