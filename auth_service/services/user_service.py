from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import uuid
from models.user import AuthUser
from core.security import verify_password, get_password_hash
from schemas.auth import UserCreate, UserResponse

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str) -> Optional[AuthUser]:
        """Получение пользователя по username"""
        stmt = select(AuthUser).where(AuthUser.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[AuthUser]:
        """Получение пользователя по ID"""
        stmt = select(AuthUser).where(AuthUser.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[AuthUser]:
        """Получение пользователя по email"""
        stmt = select(AuthUser).where(AuthUser.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def authenticate_user(self, username: str, password: str) -> Optional[AuthUser]:
        """Аутентификация пользователя"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user

    async def create_user(self, user_data: UserCreate) -> AuthUser:
        """Создание нового пользователя"""
        # Проверяем, нет ли уже пользователя с таким username или email
        existing_user = await self.get_user_by_username(user_data.username)
        if existing_user:
            raise ValueError("User with this username already exists")
        
        existing_email = await self.get_user_by_email(user_data.email)
        if existing_email:
            raise ValueError("User with this email already exists")
        
        # Создаем пользователя
        hashed_password = get_password_hash(user_data.password)
        user = AuthUser(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def create_user_from_event(self, user_data: dict) -> AuthUser:
        """Создание пользователя из события (уже с хешированным паролем)"""
        user = AuthUser(
            id=user_data["user_id"],
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=user_data["password"],  # Пароль уже хеширован
            created_at=user_data["created_at"],
            role=user_data["role"]
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def update_user_last_login(self, user_id: uuid.UUID):
        """Обновление времени последнего входа"""
        user = await self.get_user_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            await self.db.commit()

    async def update_user_from_event(self, user_data: dict):
        """Обновление пользователя из события"""
        user = await self.get_user_by_id(user_data["user_id"])
        if not user:
            return None
        
        if "username" in user_data and user_data["username"]:
            user.username = user_data["username"]
        
        if "email" in user_data and user_data["email"]:
            user.email = user_data["email"]
        
        if "password" in user_data and user_data["password"]:
            user.hashed_password = get_password_hash(user_data["password"])
        
        if "is_active" in user_data:
            user.is_active = user_data["is_active"]
        
        user.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def delete_user(self, user_id: uuid.UUID):
        """Удаление пользователя"""
        user = await self.get_user_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()