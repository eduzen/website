from unittest import mock

from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from core.middleware import CloudflareRealIPMiddleware, _is_cloudflare_addr


class TestCloudflareMiddleware(TestCase):
    def setUp(self) -> None:
        self.get_response = mock.MagicMock(return_value=HttpResponse("ok"))
        self.middleware = CloudflareRealIPMiddleware(self.get_response)
        super().setUp()

    def test_request_ip_uses_cf_connecting_ip(self) -> None:
        request = RequestFactory().get("/", HTTP_CF_CONNECTING_IP="123.123.123.123")

        self.middleware(request)

        assert hasattr(request, "ip") and request.ip == "123.123.123.123"

    def test_request_ip_falls_back_to_remote_addr(self) -> None:
        request = RequestFactory().get("/")

        self.middleware(request)

        assert request.ip == "127.0.0.1"

    def test_replaces_remote_addr_when_proxy_is_cloudflare(self) -> None:
        request = RequestFactory().get(
            "/",
            HTTP_CF_CONNECTING_IP="203.0.113.99",
            REMOTE_ADDR="173.245.48.5",
        )

        self.middleware(request)

        assert request.META["REMOTE_ADDR"] == "203.0.113.99"
        assert request.ip == "203.0.113.99"

    def test_does_not_replace_remote_addr_when_proxy_is_not_cloudflare(self) -> None:
        request = RequestFactory().get(
            "/",
            HTTP_CF_CONNECTING_IP="203.0.113.99",
            REMOTE_ADDR="198.51.100.8",
        )

        self.middleware(request)

        assert request.META["REMOTE_ADDR"] == "198.51.100.8"
        assert request.ip == "203.0.113.99"

    def test_does_not_replace_with_cloudflare_to_cloudflare_hop(self) -> None:
        request = RequestFactory().get(
            "/",
            HTTP_CF_CONNECTING_IP="173.245.48.9",
            REMOTE_ADDR="173.245.48.5",
        )

        self.middleware(request)

        assert request.META["REMOTE_ADDR"] == "173.245.48.5"
        assert request.ip == "173.245.48.9"

    def test_cloudflare_addr_helper_handles_invalid_values(self) -> None:
        assert _is_cloudflare_addr("173.245.48.10") is True
        assert _is_cloudflare_addr("198.51.100.10") is False
        assert _is_cloudflare_addr("not-an-ip") is False
