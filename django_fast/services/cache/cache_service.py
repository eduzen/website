# services/caches.py
import abc
import datetime
from typing import Any

from django.core.cache import caches


class AbstractCacheService(abc.ABC):
    """Interface for cache services, enforcing the methods all backends must implement."""

    def __init__(self, alias: str):
        self.alias = alias
        self.cache = caches[alias]  # Django's cache instance

    @abc.abstractmethod
    def ping(self) -> bool:
        """Check if the cache backend is available. Returns True if alive."""
        pass

    @abc.abstractmethod
    def clear_cache(self) -> None:
        """Clears (flushes) the cache for this alias."""
        pass

    @abc.abstractmethod
    def get_stats(self) -> dict[str, Any]:
        """Retrieves relevant statistics for this cache backend."""
        pass


class RedisCacheService(AbstractCacheService):
    """Redis-specific implementation."""

    def __init__(self, alias: str, redis_connection=None):
        super().__init__(alias)
        self.redis_connection = redis_connection

    def ping(self) -> bool:
        if self.redis_connection:
            try:
                return self.redis_connection.ping() is True
            except Exception:
                return False
        else:
            # Fallback: do a simple set/get using Django’s cache if supported
            try:
                self.cache.set("redis_ping_check", "ok", timeout=5)
                return self.cache.get("redis_ping_check") == "ok"
            except Exception:
                return False

    def clear_cache(self) -> None:
        self.cache.clear()

    def get_stats(self) -> dict[str, Any]:
        stats = {}
        if self.redis_connection:
            # Example: gather memory and keyspace info from direct Redis connection
            try:
                mem_info = self.redis_connection.info("memory")
                stats["used_memory_human"] = mem_info.get("used_memory_human", "N/A")
                stats["used_memory_peak_human"] = mem_info.get("used_memory_peak_human", "N/A")

                keyspace_info = self.redis_connection.info("keyspace")
                readable_keyspace = {}
                for db, db_stats in keyspace_info.items():
                    readable_keyspace[db] = db_stats.copy()
                    if "avg_ttl" in db_stats:
                        readable_keyspace[db]["avg_ttl"] = self._format_ttl(db_stats["avg_ttl"])

                stats["keyspace"] = readable_keyspace
                # total keys
                stats["dbsize"] = self.redis_connection.dbsize()
            except Exception as exc:
                stats["error"] = str(exc)
        else:
            # Fallback using Django’s cache interface (limited: .keys, .ttl)
            try:
                all_keys = self.cache.keys("*")
                stats["keys_count"] = len(all_keys)
                stats["sample_ttl"] = {k: self.cache.ttl(k) for k in all_keys[:5]}
            except AttributeError:
                stats["message"] = "Backend does not support .keys() or .ttl()."
        return stats

    def _format_ttl(self, ttl_ms: int) -> str:
        """Convert TTL from milliseconds to a more readable format."""
        ttl_seconds = ttl_ms / 1000
        return str(datetime.timedelta(seconds=ttl_seconds))


class MemcachedService(AbstractCacheService):
    """Memcached-specific implementation."""

    def ping(self) -> bool:
        # Memcached typically doesn't have a "ping".
        # We can do a set/get test or see if your memcache library has a "check_key" or "stats" method.
        try:
            self.cache.set("memcached_ping_check", "ok", timeout=5)
            return self.cache.get("memcached_ping_check") == "ok"
        except Exception:
            return False

    def clear_cache(self) -> None:
        self.cache.clear()

    def get_stats(self) -> dict[str, Any]:
        # Memcached might support .stats() if you have a direct client.
        # django-pylibmc or python-memcached might let you do:
        #    self.cache._cache.get_stats()
        # But this is very library-specific.
        try:
            mem_stats = self.cache._cache.get_stats()
            # parse results
            return {"raw_stats": mem_stats}
        except Exception:
            return {"message": "Stats not available for memcached or library not supported."}


class DatabaseCacheService(AbstractCacheService):
    """Database-backed cache (using Django's built-in DB caching)."""

    def ping(self) -> bool:
        # We can do a set/get test. If DB is unavailable, we'll get an error.
        try:
            self.cache.set("db_cache_ping_check", "ok", timeout=5)
            return self.cache.get("db_cache_ping_check") == "ok"
        except Exception:
            return False

    def clear_cache(self) -> None:
        self.cache.clear()

    def get_stats(self) -> dict[str, Any]:
        # Not much to do here. Possibly query the table for row count, etc.
        # For instance, the DB cache uses a table (default: django_cache_table).
        # You might do a direct DB query here if you want row counts, etc.
        return {"message": "Database cache does not provide detailed stats by default."}


class FileBasedCacheService(AbstractCacheService):
    """File system-based cache."""

    def ping(self) -> bool:
        # Setting/Getting a key should suffice as a "ping".
        try:
            self.cache.set("file_cache_ping_check", "ok", timeout=5)
            return self.cache.get("file_cache_ping_check") == "ok"
        except Exception:
            return False

    def clear_cache(self) -> None:
        self.cache.clear()

    def get_stats(self) -> dict[str, Any]:
        # Possibly do a directory walk to count files, check disk usage, etc.
        return {"message": "File-based cache does not provide advanced stats by default."}


class DummyCacheService(AbstractCacheService):
    """Dummy cache is typically used in dev (it never stores anything)."""

    def ping(self) -> bool:
        # It's always "alive" but basically does nothing.
        return True

    def clear_cache(self) -> None:
        # No-op
        pass

    def get_stats(self) -> dict[str, Any]:
        return {"message": "Dummy cache does not store data."}