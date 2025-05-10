from unittest import mock

from django.test import TestCase
from django.test.client import RequestFactory

from core.middleware import CloudflareRealIPMiddleware


class TestCloudflareMiddleware(TestCase):
    def setUp(self) -> None:
        self.get_response = mock.MagicMock()
        self.middleware = CloudflareRealIPMiddleware(self.get_response)
        super().setUp()

    def test_requestProcessing(self):
        """Test that the client IP is correctly set from CF-Connecting-IP."""
        # Django's RequestFactory expects headers to be prefixed with HTTP_
        request = RequestFactory().get("/", HTTP_CF_CONNECTING_IP="123.123.123.123")
        self.middleware(request)
        assert hasattr(request, "ip") and request.ip == "123.123.123.123"

    def test_fallback_to_remote_addr(self):
        """Test that the client IP falls back to REMOTE_ADDR if CF-Connecting-IP is not present."""
        request = RequestFactory().get("/")
        self.middleware(request)
        assert request.ip == "127.0.0.1"
