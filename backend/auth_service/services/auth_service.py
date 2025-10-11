"""служба верификации токенов с возвращением роли"""#pylint: disable=E0611, E0401
from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from auth_service.schemas.messaging import (
    TokenVerifyMessage,
    TokenVerifyResponseMessage
)

class AuthService:
    """класс обработки сообщений верификации"""
    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    async def verify_token_handler(self, message: TokenVerifyMessage) -> TokenVerifyResponseMessage:
        """Обработчик верификации токена"""
        result = await self.token_service.verify_access_token(message.token)

        user = await self.user_service.get_user_by_id(result.get("user_id"))
        role = user.role

        return TokenVerifyResponseMessage(
            valid=result["valid"],
            user_id=result.get("user_id"),
            error=result.get("error"),
            role = role
        )
