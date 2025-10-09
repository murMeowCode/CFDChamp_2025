from authentication_service.services.token_service import TokenService
from authentication_service.services.user_service import UserService
from authentication_service.schemas.messaging import (
    TokenVerifyMessage, 
    TokenVerifyResponseMessage,
    TokenRefreshMessage,
    TokenRefreshResponseMessage,
    UserCreatedMessage
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

    async def refresh_token_handler(self, message: TokenRefreshMessage) -> TokenRefreshResponseMessage:
        """Обработчик обновления токенов"""
        result = await self.token_service.refresh_tokens(message.refresh_token)
        
        return TokenRefreshResponseMessage(
            success=result["success"],
            access_token=result.get("tokens", {}).get("access_token"),
            refresh_token=result.get("tokens", {}).get("refresh_token"),
            error=result.get("error")
        )
    
    async def handle_user_created(self, message: UserCreatedMessage):
        """Обработчик создания пользователя"""
        try:
            # Хешируем пароль перед сохранением
            from authentication_service.core.security import get_password_hash
            hashed_password = get_password_hash(message.password)
            
            user_data = {
                "user_id": message.user_id,
                "username": message.username,
                "email": message.email,
                "password": hashed_password,  # Сохраняем хешированный пароль
                "created_at": message.created_at,
                "role": message.role
            }
            
            await self.user_service.create_user_from_event(user_data)
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
