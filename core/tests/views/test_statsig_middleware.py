from __future__ import annotations

from typing import Any, cast
from unittest import mock

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory, TestCase

from core.middleware import StatsigAnalyticsMiddleware


class _DummyHtmxDetails:
    def __init__(self, *, history_restore_request: bool = False) -> None:
        self.history_restore_request = history_restore_request

    def __bool__(self) -> bool:
        return True


class TestStatsigAnalyticsMiddleware(TestCase):
    def setUp(self) -> None:
        self.get_response = mock.MagicMock(return_value=HttpResponse("ok", status=200))
        self.middleware = StatsigAnalyticsMiddleware(self.get_response)
        self.resolver = mock.MagicMock()
        self.resolver.url_name = "home"
        self.resolver.view_name = "blog.views.HomeView"
        self.resolver.kwargs = {}
        super().setUp()

    def _build_request(
        self,
        *,
        path: str = "/",
        method: str = "GET",
        user: User | AnonymousUser | None = None,
    ) -> HttpRequest:
        request = RequestFactory().generic(method, path)
        request.resolver_match = self.resolver
        request.user = user if user is not None else AnonymousUser()
        request.session = SessionStore(session_key="session-key")
        request.LANGUAGE_CODE = "en"
        request_with_htmx = cast(Any, request)
        request_with_htmx.htmx = False
        return request

    @mock.patch("core.middleware.log_event")
    def test_logs_page_view_for_successful_get(self, mock_log_event: mock.MagicMock) -> None:
        request = self._build_request()

        self.middleware(request)

        mock_log_event.assert_called_once()
        assert mock_log_event.call_args.args[1] == "page_view"
        metadata = mock_log_event.call_args.kwargs["metadata"]
        assert metadata["url_name"] == "home"
        assert metadata["path"] == "/"
        assert metadata["htmx"] == "false"

    @mock.patch("core.middleware.log_event")
    def test_skips_non_get_requests(self, mock_log_event: mock.MagicMock) -> None:
        request = self._build_request(method="POST")

        self.middleware(request)

        mock_log_event.assert_not_called()

    @mock.patch("core.middleware.log_event")
    def test_skips_non_200_responses(self, mock_log_event: mock.MagicMock) -> None:
        self.get_response.return_value = HttpResponse("missing", status=404)
        request = self._build_request()

        self.middleware(request)

        mock_log_event.assert_not_called()

    @mock.patch("core.middleware.log_event")
    def test_skips_htmx_history_restore_requests(self, mock_log_event: mock.MagicMock) -> None:
        request = self._build_request()
        request_with_htmx = cast(Any, request)
        request_with_htmx.htmx = _DummyHtmxDetails(history_restore_request=True)

        self.middleware(request)

        mock_log_event.assert_not_called()

    @mock.patch("core.middleware.log_event")
    def test_skips_static_paths(self, mock_log_event: mock.MagicMock) -> None:
        request = self._build_request(path="/static/core/css/base.css")

        self.middleware(request)

        mock_log_event.assert_not_called()

    @mock.patch("core.middleware.log_event")
    def test_logs_admin_page_view_for_staff_user(self, mock_log_event: mock.MagicMock) -> None:
        staff_user = User(is_staff=True, is_superuser=True)
        request = self._build_request(path="/admin/", user=staff_user)
        self.resolver.url_name = "admin:index"
        self.resolver.view_name = "django.contrib.admin.sites.index"

        self.middleware(request)

        assert mock_log_event.call_count == 2
        assert mock_log_event.call_args_list[0].args[1] == "page_view"
        assert mock_log_event.call_args_list[1].args[1] == "admin_page_view"

    @mock.patch("core.middleware.log_event")
    def test_does_not_log_admin_page_view_for_anonymous_user(self, mock_log_event: mock.MagicMock) -> None:
        request = self._build_request(path="/admin/")
        self.resolver.url_name = "admin:index"
        self.resolver.view_name = "django.contrib.admin.sites.index"

        self.middleware(request)

        mock_log_event.assert_called_once()
        assert mock_log_event.call_args.args[1] == "page_view"

    @mock.patch("core.middleware.log_event")
    def test_includes_resolver_kwargs_in_metadata(self, mock_log_event: mock.MagicMock) -> None:
        self.resolver.url_name = "post_detail"
        self.resolver.view_name = "blog.views.PostDetailView"
        self.resolver.kwargs = {"post_id": "42"}
        request = self._build_request(path="/blog/post/42/")

        self.middleware(request)

        metadata = mock_log_event.call_args.kwargs["metadata"]
        assert metadata["post_id"] == "42"
