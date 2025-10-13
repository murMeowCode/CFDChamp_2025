"""общий модуль для аутентификации"""#pylint: disable=E0401, E0611, W0707
from typing import Optional
import uuid
from fastapi import HTTPException, Depends, Header
from shared.messaging.producers import AuthProducer
from shared.config.base import settings

class AuthDependency:
    """зависимость аутентификации"""
    def __init__(self, producer: AuthProducer):
        self.producer = producer

    async def get_current_user(
        self,
        authorization: Optional[str] = Header(None)
    ) -> dict:
        """Проверяет токен и возвращает данные пользователя"""
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        try:
            # Извлекаем токен из заголовка
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")

            # Отправляем запрос на верификацию
            response = await self.producer.verify_token(token)

            if not response.valid:
                raise HTTPException(status_code=401, detail="Invalid token")

            if not response.user_id:
                raise HTTPException(status_code=401, detail="User not found")

            return {
                "user_id": uuid.UUID(response.user_id),
                "role": response.role or 0
            }

        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        except TimeoutError:
            raise HTTPException(status_code=503, detail="Authentication service unavailable")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

    async def require_role(self, required_role: int,
                           user: dict = Depends(get_current_user)) -> dict:
        """Проверяет роль пользователя"""
        if user.get("role", 0) != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

def get_auth_dependency() -> AuthDependency:
    """Фабрика для создания AuthDependency"""
    producer = AuthProducer(rabbitmq_url=settings.RABBITMQ_URL)  # Создаем producer с настройками
    return AuthDependency(producer)
