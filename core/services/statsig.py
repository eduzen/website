from __future__ import annotations

import atexit
import logging
import os
import re

from django.conf import settings
from django.http import HttpRequest
from statsig_python_core import Statsig, StatsigOptions, StatsigUser

logger = logging.getLogger(__name__)

_PLACEHOLDER_SECRETS = {"", "foo", "changeme", "somekey", "secret-key"}

_initialized_pid: int | None = None
_shutdown_registered = False

_TABLET_RE = re.compile(r"ipad|tablet|playbook|silk", re.IGNORECASE)
_MOBILE_RE = re.compile(r"mobile|iphone|ipod|android.*mobile|windows phone|blackberry", re.IGNORECASE)


def detect_device_type(user_agent: str) -> str:
    if not user_agent:
        return "unknown"
    if _TABLET_RE.search(user_agent):
        return "tablet"
    if _MOBILE_RE.search(user_agent):
        return "mobile"
    return "desktop"


def _has_valid_secret(secret: str) -> bool:
    return bool(secret and secret not in _PLACEHOLDER_SECRETS)


def _is_configured() -> bool:
    return bool(
        getattr(settings, "STATSIG_ENABLED", False)
        and _has_valid_secret(getattr(settings, "STATSIG_SERVER_SECRET", ""))
    )


def _register_shutdown() -> None:
    global _shutdown_registered
    if _shutdown_registered:
        return
    atexit.register(shutdown_statsig)
    _shutdown_registered = True


def _ensure_initialized() -> bool:
    global _initialized_pid

    if not _is_configured():
        return False

    pid = os.getpid()
    if _initialized_pid == pid:
        return Statsig.has_shared_instance()

    if Statsig.has_shared_instance():
        Statsig.remove_shared()

    environment = getattr(settings, "STATSIG_ENVIRONMENT", "development")
    server_secret = getattr(settings, "STATSIG_SERVER_SECRET", "")

    options = StatsigOptions()
    options.environment = environment

    statsig = Statsig.new_shared(server_secret, options)
    statsig.initialize().wait()
    _initialized_pid = pid
    _register_shutdown()
    logger.info("Statsig initialized for pid=%s environment=%s", pid, environment)
    return True


def get_client() -> Statsig | None:
    if not _ensure_initialized():
        return None

    return Statsig.shared()


def shutdown_statsig() -> None:
    global _initialized_pid

    if not Statsig.has_shared_instance():
        return

    try:
        Statsig.shared().shutdown().wait()
        logger.info("Statsig shutdown complete for pid=%s", os.getpid())
    except Exception:
        logger.exception("Statsig shutdown failed")
    finally:
        Statsig.remove_shared()
        _initialized_pid = None


def build_user(request: HttpRequest) -> StatsigUser:
    user_agent = request.headers.get("user-agent", "")
    user_id = "anonymous"

    if getattr(request, "user", None) and request.user.is_authenticated:
        user_id = str(request.user.pk)
    elif request.session.session_key:
        user_id = request.session.session_key

    ip = getattr(request, "ip", None) or request.META.get("REMOTE_ADDR")
    locale = getattr(request, "LANGUAGE_CODE", None)

    return StatsigUser(
        user_id=user_id,
        ip=ip,
        user_agent=user_agent,
        locale=locale,
        custom={"device_type": detect_device_type(user_agent)},
    )


def log_event(
    request: HttpRequest,
    event_name: str,
    *,
    value: str | None = None,
    metadata: dict[str, str] | None = None,
) -> None:
    client = get_client()
    if client is None:
        return

    try:
        client.log_event(
            user=build_user(request),
            event_name=event_name,
            value=value,
            metadata=metadata,
        )
    except Exception:
        logger.exception("Statsig log_event failed for event=%s", event_name)


def check_gate(request: HttpRequest, gate_name: str) -> bool:
    client = get_client()
    if client is None:
        return False

    try:
        return client.check_gate(build_user(request), gate_name)
    except Exception:
        logger.exception("Statsig check_gate failed for gate=%s", gate_name)
        return False
