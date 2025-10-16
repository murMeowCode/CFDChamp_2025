"""Модуль для работы с Redis кэшированием."""
import json
from functools import wraps
from typing import Any, Callable
from shared.utils.redis_client import get_cache_redis


def cache_response(prefix: str, ttl: int = 300) -> Callable:
    """Декоратор для кэширования ответов API."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            redis = await get_cache_redis()
            cache_key = f"{prefix}:"

            user_id = None
            for arg in args:
                if isinstance(arg, dict) and "user_id" in arg:
                    user_id = arg["user_id"]
                    break

            if user_id:
                cache_key += f"user:{user_id}"
            else:
                cache_key += "all"

            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

            result = await func(*args, **kwargs)

            await redis.setex(
                cache_key, 
                ttl, 
                json.dumps(
                    result if not hasattr(result, 'dict') else result.dict(),
                    default=str
                )
            )

            return result
        return wrapper
    return decorator


async def invalidate_user_cache(user_id: str) -> None:
    """Инвалидирует кэш для конкретного пользователя."""
    redis = await get_cache_redis()
    user_key = f"profile:user:{user_id}"
    all_users_key = "profile:all"

    await redis.delete(user_key)
    await redis.delete(all_users_key)


async def invalidate_all_profiles_cache() -> None:
    """Инвалидирует кэш всех профилей."""
    redis = await get_cache_redis()
    all_users_key = "profile:all"
    await redis.delete(all_users_key)


async def invalidate_pattern_cache(pattern: str) -> None:
    """Инвалидирует кэш по паттерну."""
    redis = await get_cache_redis()
    keys = []

    async for key in redis.scan_iter(match=f"*{pattern}*"):
        keys.append(key)

    if keys:
        await redis.delete(*keys)
