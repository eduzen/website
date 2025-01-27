# services/cache/factory.py
import logfire
import redis
from django.conf import settings

from .cache_service import (
    AbstractCacheService,
    DatabaseCacheService,
    DummyCacheService,
    FileBasedCacheService,
    MemcachedService,
    RedisCacheService,
)


def get_cache_service(alias: str) -> AbstractCacheService:
    """Return an instance of the appropriate cache service class based on settings."""
    cache_config = settings.CACHES[alias]
    backend = cache_config["BACKEND"]

    if "RedisCache" in backend:
        logfire.info(f"Creating RedisCacheService for alias '{alias}'")
        # or possibly parse connection options from `cache_config['LOCATION']` or `cache_config['OPTIONS']`.
        try:
            url = settings.CACHES["default"]["LOCATION"]
            options = cache_config.get("OPTIONS", {})
            password = options.get("PASSWORD", None)
            db = options.get("DB", 0)
            socket_timeout = options.get("SOCKET_TIMEOUT", None)
            # simplistic example
            r_client = redis.Redis.from_url(
                url=url,
                password=password,
                db=db,
                socket_timeout=socket_timeout,
            )
            # Test the connection
            if not r_client.ping():
                logfire.error(f"Redis server at '{url}' is not responding to PING.")
                raise ConnectionError(f"Cannot connect to Redis server at '{url}'.")

            return RedisCacheService(alias, redis_connection=r_client)
        except Exception as e:
            logfire.exception(f"Error creating Redis client for alias '{alias}': {e}")
            raise RuntimeError(f"Failed to initialize RedisCacheService for alias '{alias}': {e}") from e

    elif "MemcachedCache" in backend:
        logfire.info(f"Creating MemcachedService for alias '{alias}'")
        return MemcachedService(alias)

    elif "DatabaseCache" in backend:
        logfire.info(f"Creating DatabaseCacheService for alias '{alias}'")
        return DatabaseCacheService(alias)

    elif "FileBasedCache" in backend:
        logfire.info(f"Creating FileBasedCacheService for alias '{alias}'")
        return FileBasedCacheService(alias)

    elif "DummyCache" in backend:
        logfire.info(f"Creating DummyCacheService for alias '{alias}'")
        return DummyCacheService(alias)

    # Fallback if unrecognized
    logfire.warning(f"Unrecognized cache backend '{backend}' for alias '{alias}'. Falling back to DummyCacheService.")
    return DummyCacheService(alias)
