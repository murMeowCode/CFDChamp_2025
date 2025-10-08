from services.token_service import TokenService
from schemas.messaging import (
    TokenVerifyMessage, 
    TokenVerifyResponseMessage,
    TokenRefreshMessage,
    TokenRefreshResponseMessage
)

class AuthService:
    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    async def verify_token_handler(self, message: TokenVerifyMessage) -> TokenVerifyResponseMessage:
        """Обработчик верификации токена"""
        result = await self.token_service.verify_access_token(message.token)
        
        return TokenVerifyResponseMessage(
            valid=result["valid"],
            user_id=result.get("user_id"),
            error=result.get("error")
        )

    async def refresh_token_handler(self, message: TokenRefreshMessage) -> TokenRefreshResponseMessage:
        """Обработчик обновления токенов"""
        result = await self.token_service.refresh_tokens(message.refresh_token)
        
        return TokenRefreshResponseMessage(
            success=result["success"],
            access_token=result.get("tokens", {}).get("access_token"),
            refresh_token=result.get("tokens", {}).get("refresh_token"),
            error=result.get("error")
        )