import redis
from app.core.config import get_settings

_settings = get_settings()


def get_redis_client() -> redis.Redis:
    """Return a Redis client instance."""
    return redis.Redis(
        host=_settings.REDIS_HOST,
        port=_settings.REDIS_PORT,
        decode_responses=True,
    )
