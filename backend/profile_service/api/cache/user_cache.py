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

            # Способ 1: Ищем user_id в kwargs (из Depends)
            if 'user' in kwargs and isinstance(kwargs['user'], dict) and 'user_id' in kwargs['user']:
                user_id = kwargs['user']['user_id']
                cache_key+=str(user_id)
                print(f"🔑 User_id найден в kwargs: {user_id}")

            # Способ 2: Ищем user_id в args
            if not user_id:
                for arg in args:
                    if isinstance(arg, dict) and 'user_id' in arg:
                        user_id = arg['user_id']
                        print(f"🔑 User_id найден в args: {user_id}")
                        break

            # Способ 3: Для эндпоинта /all используем специальный ключ
            if func.__name__ == 'get_all_users':
                cache_key += "all"
                print("🏢 Кэш для всех пользователей")

            # Логирование попытки получения из кэша
            print(f"🔍 Поиск в кэше: {cache_key}")

            cached_data = await redis.get(cache_key)
            if cached_data:
                print(f"✅ Данные получены из кэша: {cache_key}")
                try:
                    data = json.loads(cached_data)
                    if isinstance(data, list):
                        print(f"📋 Получен список из {len(data)} элементов из кэша")
                    else:
                        print("📄 Получен одиночный объект из кэша")
                    return data
                except json.JSONDecodeError as e:
                    print(f"❌ Ошибка десериализации кэша: {e}")
            else:
                print(f"❌ Данных нет в кэше: {cache_key}")

            # Выполнение оригинальной функции
            print(f"🔄 Выполнение функции {func.__name__}")
            result = await func(*args, **kwargs)

            # Сохранение в кэш
            try:
                if hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
                    serializable_result = [item.dict() if hasattr(item, 'dict') else item for item in result]
                    print(f"📦 Сохранение списка из {len(serializable_result)} элементов в кэш")
                else:
                    serializable_result = result.dict() if hasattr(result, 'dict') else result
                    print("📄 Сохранение одиночного объекта в кэш")

                await redis.setex(
                    cache_key,
                    ttl,
                    json.dumps(serializable_result, default=str)
                )
                print(f"💾 Данные сохранены в кэш: {cache_key} (TTL: {ttl}сек)")
            except Exception as e:
                print(f"⚠️ Ошибка сохранения в кэш {cache_key}: {e}")

            return result
        return wrapper
    return decorator


async def invalidate_user_cache(user_id: str) -> None:
    """Инвалидирует кэш для конкретного пользователя."""
    try:
        redis = await get_cache_redis()
        user_key = f"profile:user:{user_id}"

        deleted_count = await redis.delete(user_key)
        print(f"🗑️ Инвалидирован кэш пользователя {user_id}. Удалено ключей: {deleted_count}")
    except Exception as e:
        print(f"⚠️ Ошибка при инвалидации кэша пользователя {user_id}: {e}")


async def invalidate_all_profiles_cache() -> None:
    """Инвалидирует кэш всех профилей."""
    try:
        redis = await get_cache_redis()
        all_users_key = "profile:all"

        deleted_count = await redis.delete(all_users_key)
        print(f"🗑️ Инвалидирован кэш всех профилей. Удалено ключей: {deleted_count}")
    except Exception as e:
        print(f"⚠️ Ошибка при инвалидации кэша всех профилей: {e}")

async def invalidate_pattern_cache(pattern: str) -> None:
    """Инвалидирует кэш по паттерну."""
    redis = await get_cache_redis()
    keys = []

    async for key in redis.scan_iter(match=f"*{pattern}*"):
        keys.append(key)

    if keys:
        await redis.delete(*keys)
