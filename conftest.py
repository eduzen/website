import pytest

from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture()
def api_client():
    """A Django RestFramework test client instance."""

    return APIClient()


@pytest.fixture()
def api_rf():
    """A Django RestFramework RequestFactory instance"""

    return APIRequestFactory()
