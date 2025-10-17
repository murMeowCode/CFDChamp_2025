import secrets
import httpx
from typing import Optional, Dict, Any
from shared.config.base import settings

class VKOAuthService:
    """Сервис для работы с VK OAuth API"""

    @staticmethod
    def generate_state() -> str:
        """Генерация случайного state для защиты от CSRF"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def get_auth_url(state: str) -> str:
        """Получение URL для перенаправления на VK OAuth"""
        base_url = "https://oauth.vk.com/authorize"
        params = {
            "client_id": settings.VK_CLIENT_ID,
            "redirect_uri": settings.VK_REDIRECT_URI,
            "display": "page",
            "scope": "email",  # Запрашиваем доступ к email
            "response_type": "code",
            "state": state,
            "v": "5.131"  # Версия API
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"

    @staticmethod
    async def get_access_token(code: str) -> Optional[Dict[str, Any]]:
        """Обмен authorization code на access token """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://oauth.vk.com/access_token",
                    params={
                        "client_id": settings.VK_CLIENT_ID,
                        "client_secret": settings.VK_CLIENT_SECRET,
                        "redirect_uri": settings.VK_REDIRECT_URI,
                        "code": code
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()

                    # Проверяем наличие ошибки
                    if "error" in data:
                        error_msg = data.get("error_description", "Unknown VK error")
                        print(f"VK OAuth error: {error_msg}")
                        return None

                    # Успешный ответ содержит access_token и user_id
                    if "access_token" in data and "user_id" in data:
                        return data

                print(f"VK OAuth failed with status: {response.status_code}")
                return None

            except httpx.TimeoutException:
                print("VK OAuth timeout")
                return None
            except Exception as e:
                print(f"VK OAuth exception: {e}")
                return None

    @staticmethod
    async def get_user_info(access_token: str, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение информации о пользователе VK"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.vk.com/method/users.get",
                    params={
                        "user_ids": user_id,
                        "fields": "photo_200,email,first_name,last_name",  # Запрашиваемые поля
                        "access_token": access_token,
                        "v": "5.131"
                    },
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()

                    # Проверяем наличие ошибки API
                    if "error" in data:
                        error_msg = data["error"].get("error_msg", "Unknown VK API error")
                        print(f"VK API error: {error_msg}")
                        return None

                    # Успешный ответ содержит массив пользователей
                    if "response" in data and len(data["response"]) > 0:
                        user_info = data["response"][0]

                        # Добавляем user_id если его нет в ответе
                        if "id" not in user_info:
                            user_info["id"] = user_id

                        return user_info

                print(f"VK API failed with status: {response.status_code}")
                return None

            except httpx.TimeoutException:
                print("VK API timeout")
                return None
            except Exception as e:
                print(f"VK API exception: {e}")
                return None

    @staticmethod
    def validate_oauth_response(response_data: Dict[str, Any]) -> bool:
        """Валидация ответа от VK OAuth"""
        required_fields = ["access_token", "user_id"]
        return all(field in response_data for field in required_fields)

    @staticmethod
    def validate_user_info(user_info: Dict[str, Any]) -> bool:
        """Валидация информации о пользователе от VK API"""
        required_fields = ["first_name", "last_name"]
        return all(field in user_info for field in required_fields)