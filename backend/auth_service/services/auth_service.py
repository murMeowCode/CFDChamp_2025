from auth_service.services.token_service import TokenService
from auth_service.services.user_service import UserService
from auth_service.schemas.messaging import (
    TokenVerifyMessage, 
    TokenVerifyResponseMessage
)

class AuthService:
    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    async def verify_token_handler(self, message: TokenVerifyMessage) -> TokenVerifyResponseMessage:
        """Обработчик верификации токена"""
        result = await self.token_service.verify_access_token(message.token)
        
        return TokenVerifyResponseMessage(
            valid=result["valid"],
            user_id=result.get("user_id"),
            error=result.get("error")
        )
