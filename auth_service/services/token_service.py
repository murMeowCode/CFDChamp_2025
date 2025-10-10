from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import uuid
from models.token import RefreshToken
from core.security import create_access_token, create_refresh_token, verify_token
from shared.config.base import settings

class TokenService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_token_pair(self, user_id: str, username: str) -> dict:
        """Создание пары access/refresh токенов"""
        
        # Создаем access token
        access_token = create_access_token(
            data={"sub": user_id, "username": username}
        )
        
        # Создаем refresh token
        refresh_token_data = {"sub": user_id, "token_id": str(uuid.uuid4())}
        refresh_token = create_refresh_token(refresh_token_data)
        
        # Сохраняем refresh token в БД
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db_refresh_token = RefreshToken(
            user_id=uuid.UUID(user_id),
            token=refresh_token,
            expires_at=expires_at
        )
        
        self.db.add(db_refresh_token)
        await self.db.commit()
        await self.db.refresh(db_refresh_token)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def verify_access_token(self, token: str) -> dict:
        """Проверка access token"""
        payload = verify_token(token)
        if not payload:
            return {"valid": False, "error": "Invalid token"}
        
        if payload.get("type") != "access":
            return {"valid": False, "error": "Not an access token"}
        
        return {
            "valid": True, 
            "user_id": payload.get("sub"),
            "username": payload.get("username")
        }

    async def refresh_tokens(self, refresh_token: str) -> dict:
        """Обновление пары токенов"""
        
        # Проверяем refresh token
        payload = verify_token(refresh_token)
        if not payload:
            return {"success": False, "error": "Invalid refresh token"}
        
        if payload.get("type") != "refresh":
            return {"success": False, "error": "Not a refresh token"}
        
        # Проверяем наличие в БД
        stmt = select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.is_active == True
        )
        result = await self.db.execute(stmt)
        db_token = result.scalar_one_or_none()
        
        if not db_token or db_token.is_expired():
            return {"success": False, "error": "Refresh token expired or revoked"}
        
        # Деактивируем старый refresh token
        db_token.is_active = False
        await self.db.commit()
        
        # Создаем новую пару токенов
        user_id = str(db_token.user_id)
        new_tokens = await self.create_token_pair(user_id, "")
        
        return {
            "success": True,
            "tokens": new_tokens
        }

    async def cleanup_expired_tokens(self):
        """Очистка просроченных токенов"""
        from sqlalchemy import delete
        
        stmt = delete(RefreshToken).where(
            RefreshToken.expires_at < datetime.utcnow()
        )
        await self.db.execute(stmt)
        await self.db.commit()
