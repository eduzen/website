from __future__ import annotations

from collections.abc import Iterator
from typing import Any, cast
from unittest import mock

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.test import RequestFactory

import core.services.statsig as statsig_module
from core.services.statsig import (
    build_user,
    check_gate,
    detect_device_type,
    log_event,
    shutdown_statsig,
)

SESSION_KEY = "a" * 32


@pytest.fixture(autouse=True)
def reset_statsig_state() -> Iterator[None]:
    statsig_module._initialized_pid = None
    statsig_module._shutdown_registered = False
    yield
    shutdown_statsig()


class TestDetectDeviceType:
    def test_mobile_user_agent(self) -> None:
        assert detect_device_type("Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)") == "mobile"

    def test_tablet_user_agent(self) -> None:
        assert detect_device_type("Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)") == "tablet"

    def test_desktop_user_agent(self) -> None:
        assert detect_device_type("Mozilla/5.0 (Windows NT 10.0; Win64; x64)") == "desktop"

    def test_unknown_user_agent(self) -> None:
        assert detect_device_type("") == "unknown"


class TestBuildUser:
    def test_authenticated_user_uses_primary_key(self) -> None:
        request = RequestFactory().get("/")
        user = User(pk=42)
        request.user = user
        request.session = SessionStore(session_key=SESSION_KEY)

        statsig_user = build_user(request)

        assert statsig_user.user_id == "42"

    def test_anonymous_user_uses_session_key(self) -> None:
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.session = SessionStore(session_key=SESSION_KEY)

        statsig_user = build_user(request)

        assert statsig_user.user_id == SESSION_KEY

    def test_anonymous_user_without_session_uses_fallback(self) -> None:
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.session = SessionStore()

        statsig_user = build_user(request)

        assert statsig_user.user_id == "anonymous"

    def test_includes_device_type_and_user_agent(self) -> None:
        request = RequestFactory().get("/", HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)")
        request.user = AnonymousUser()
        request.session = SessionStore(session_key=SESSION_KEY)
        request_with_ip = cast(Any, request)
        request_with_ip.ip = "203.0.113.1"

        statsig_user = build_user(request)

        assert statsig_user.user_agent == "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        assert statsig_user.custom["device_type"] == "mobile"
        assert statsig_user.ip == "203.0.113.1"


@mock.patch("core.services.statsig.Statsig")
def test_log_event_does_not_initialize_when_disabled(mock_statsig: mock.MagicMock, settings) -> None:
    settings.STATSIG_ENABLED = False
    settings.STATSIG_SERVER_SECRET = ""

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = SessionStore(session_key=SESSION_KEY)

    log_event(request, "page_view")

    mock_statsig.new_shared.assert_not_called()


@mock.patch("core.services.statsig.Statsig")
def test_check_gate_returns_false_when_disabled(mock_statsig: mock.MagicMock, settings) -> None:
    settings.STATSIG_ENABLED = False
    settings.STATSIG_SERVER_SECRET = ""

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = SessionStore(session_key=SESSION_KEY)

    assert check_gate(request, "example_gate") is False
    mock_statsig.new_shared.assert_not_called()


@mock.patch("core.services.statsig.Statsig")
def test_log_event_initializes_and_logs(mock_statsig: mock.MagicMock, settings) -> None:
    settings.STATSIG_ENABLED = True
    settings.STATSIG_SERVER_SECRET = "server-secret-key"
    settings.STATSIG_ENVIRONMENT = "development"

    mock_client = mock.MagicMock()
    mock_statsig.new_shared.return_value = mock_client
    mock_statsig.has_shared_instance.return_value = True
    mock_statsig.shared.return_value = mock_client

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = SessionStore(session_key=SESSION_KEY)

    log_event(request, "page_view", metadata={"path": "/"})

    mock_statsig.new_shared.assert_called_once()
    mock_client.initialize.return_value.wait.assert_called_once()
    mock_client.log_event.assert_called_once()


@mock.patch("core.services.statsig.Statsig")
def test_check_gate_returns_sdk_result(mock_statsig: mock.MagicMock, settings) -> None:
    settings.STATSIG_ENABLED = True
    settings.STATSIG_SERVER_SECRET = "server-secret-key"
    settings.STATSIG_ENVIRONMENT = "development"

    mock_client = mock.MagicMock()
    mock_client.check_gate.return_value = True
    mock_statsig.new_shared.return_value = mock_client
    mock_statsig.has_shared_instance.return_value = True
    mock_statsig.shared.return_value = mock_client

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = SessionStore(session_key=SESSION_KEY)

    assert check_gate(request, "example_gate") is True
    mock_client.check_gate.assert_called_once()


@mock.patch("core.services.statsig.Statsig")
def test_placeholder_secret_is_treated_as_unconfigured(mock_statsig: mock.MagicMock, settings) -> None:
    settings.STATSIG_ENABLED = True
    settings.STATSIG_SERVER_SECRET = "somekey"
    settings.STATSIG_ENVIRONMENT = "development"

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = SessionStore(session_key=SESSION_KEY)

    log_event(request, "page_view")

    mock_statsig.new_shared.assert_not_called()
