"""Служба OAuth""" #pylint: disable=E0401,E0611, W0718
from datetime import datetime, timedelta
from typing import Any, Dict
from sqlalchemy import select
from shared.schemas.messaging import UserCreatedMessage
from shared.database.database import AsyncSession
from auth_service.models.oauth import OAuthState
from auth_service.messaging.producers import UserProducer
from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from auth_service.services.vk_oauth import VKOAuthService
from auth_service.models.user import AuthUser

class OAuthService:
    """Класс службы"""
    def __init__(self, db: AsyncSession, producer: UserProducer):
        self.db = db
        self.user_service = UserService(db)
        self.token_service = TokenService(db)
        self.vk_oauth = VKOAuthService()
        self.producer = producer

    async def create_oauth_state(self) -> str:
        """Создание и сохранение OAuth state в базе"""
        state = self.vk_oauth.generate_state()

        state_record = OAuthState(
            state=state,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )

        self.db.add(state_record)
        await self.db.commit()
        return state

    async def validate_oauth_state(self, state: str) -> bool:
        """Валидация OAuth state из базы"""
        try:
            stmt = select(OAuthState).where(OAuthState.state == state)
            result = await self.db.execute(stmt)
            state_record = result.scalar_one_or_none()

            if not state_record:
                print(f"State not found: {state}")
                return False

            if state_record.is_expired():
                print(f"State expired: {state}")
                # Удаляем просроченный state
                await self.db.delete(state_record)
                await self.db.commit()
                return False

            # Удаляем использованный state
            await self.db.delete(state_record)
            await self.db.commit()
            return True

        except Exception as e:
            print(f"Error validating state: {e}")
            return False

    async def handle_vk_oauth_callback(self, code: str) -> Dict[str, Any]:
        """Обработка callback от VK OAuth"""
        # Получаем access token
        token_data = await self.vk_oauth.get_access_token(code)
        if not token_data or "access_token" not in token_data:
            raise ValueError("Failed to get access token from VK")

        access_token = token_data["access_token"]
        vk_user_id = token_data["user_id"]
        email = token_data.get("email")

        # Получаем информацию о пользователе
        user_info = await self.vk_oauth.get_user_info(access_token, vk_user_id)
        if not user_info:
            raise ValueError("Failed to get user info from VK")

        first_name = user_info.get("first_name", "")
        last_name = user_info.get("last_name", "")
        avatar_url = user_info.get("photo_200", "")

        # Находим или создаем пользователя в auth service
        user = await self.user_service.find_or_create_oauth_user(
            vk_id=vk_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Отправляем событие в основной сервис для создания профиля
        is_new_user = user.created_at.date() == datetime.utcnow().date()

        if is_new_user:
            await self._send_oauth_user_created_event(
                user=user,
                first_name=first_name,
                last_name=last_name,
                avatar_url=avatar_url
            )

        # Обновляем время последнего входа
        await self.user_service.update_user_last_login(user.id)

        # Создаем токены
        tokens = await self.token_service.create_token_pair(
            user_id=str(user.id),
            username=user.username
        )

        return {
            "user": user,
            "tokens": tokens,
            "is_new_user": is_new_user
        }

    async def _send_oauth_user_created_event(
        self,
        user: AuthUser,
        first_name: str,
        last_name: str,
        avatar_url: str = None
    ):
        """Отправка события создания OAuth пользователя"""
        user_created_message = UserCreatedMessage(
            user_id=user.id,
            username=user.username,
            email=user.email,
            password=None,  # Пароль отсутствует
            role=user.role,
            first_name=first_name,
            last_name=last_name,
            avatar_url=avatar_url,
            middle_name=None,  # Для VK не предоставляется
            birth_date=None,   # Для VK не предоставляется
            phone=None,        # Для VK не предоставляется
            address=None      # Для VK не предоставляется
        )

        # Отправляем в основной сервис
        await self.producer.send_user_created_event(user_created_message)

        # Отправляем уведомление
        await self.producer.send_notification({
            "type": "user_registered_oauth",
            "username": user.username,
            "user_email": user.email,
            "user_id": str(user.id),
            "oauth_provider": "vk",
            "first_name": first_name,
            "last_name": last_name
        })
