import logging
from functools import wraps

from fastapi_cache import JsonCoder, FastAPICache

logger = logging.getLogger(__name__)


def log_cache_hit(cache_key: str, expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            backend = FastAPICache.get_backend()
            cached_value = await backend.get(cache_key)

            if cached_value:
                return JsonCoder.decode(cached_value)
            logger.info(f"Cache miss: {cache_key}")
            value = await func(*args, **kwargs)
            await backend.set(cache_key, JsonCoder.encode(value), expire=expire)
            return value

        return wrapper

    return decorator
