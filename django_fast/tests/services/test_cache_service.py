from unittest.mock import MagicMock

import pytest

from django_fast.services.cache.cache_service import RedisCacheService


@pytest.fixture
def mock_redis_connection() -> MagicMock:
    client = MagicMock()
    client.ping.return_value = True

    def info_side_effect(section: str) -> dict[str, object]:
        return {
            "memory": {"used_memory_human": "1.2MB", "used_memory_peak_human": "2.5MB"},
            "keyspace": {"db0": {"keys": 18, "expires": 18, "avg_ttl": 2591926923}},
        }.get(section, {})

    client.info.side_effect = info_side_effect
    client.dbsize.return_value = 18
    return client


def test_ping(mock_redis_connection: MagicMock) -> None:
    service = RedisCacheService(alias="default", redis_connection=mock_redis_connection)
    assert service.ping() is True


def test_get_stats(mock_redis_connection: MagicMock) -> None:
    service = RedisCacheService(alias="default", redis_connection=mock_redis_connection)
    stats = service.get_stats()
    assert stats["used_memory_human"] == "1.2MB"
    assert stats["used_memory_peak_human"] == "2.5MB"
    assert stats["dbsize"] == 18
    assert stats["keyspace"]["db0"]["keys"] == 18
