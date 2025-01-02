# services/cache/factory.py
import logging

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

logger = logging.getLogger(__name__)


def get_cache_service(alias: str) -> AbstractCacheService:
    """Return an instance of the appropriate cache service class based on settings."""
    cache_config = settings.CACHES[alias]
    backend = cache_config["BACKEND"]

    if "RedisCache" in backend:
        logger.info(f"Creating RedisCacheService for alias '{alias}'")
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
        except Exception:
            logger.exception("Error creating redis client.")
            r_client = None
        return RedisCacheService(alias, redis_connection=r_client)

    elif "MemcachedCache" in backend:
        return MemcachedService(alias)

    elif "DatabaseCache" in backend:
        return DatabaseCacheService(alias)

    elif "FileBasedCache" in backend:
        return FileBasedCacheService(alias)

    elif "DummyCache" in backend:
        return DummyCacheService(alias)

    # Fallback if unrecognized
    return DummyCacheService(alias)
