from unittest import mock

from django.test import TestCase
from django.test.client import RequestFactory

from core.middleware import CloudflareMiddleware


class TestCloudflareMiddleware(TestCase):
    def setUp(self) -> None:
        self.get_response = mock.MagicMock()
        self.middleware = CloudflareMiddleware(self.get_response)
        super().setUp()

    def test_requestProcessing(self):
        """Test that the client IP is correctly set from CF-Connecting-IP."""
        headers = {"CF-Connecting-IP": "123.123.123.123"}
        request = RequestFactory(headers=headers).get("/")
        self.middleware(request)
        assert request.ip == "123.123.123.123"

    def test_fallback_to_remote_addr(self):
        """Test that the client IP falls back to REMOTE_ADDR if CF-Connecting-IP is not present."""
        request = RequestFactory().get("/")
        self.middleware(request)
        assert request.ip == "127.0.0.1"
