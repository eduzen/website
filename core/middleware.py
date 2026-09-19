import ipaddress
import logging
from collections.abc import Callable
from typing import Any, Final, cast

from django.http import HttpRequest, HttpResponse

from core.htmx import is_htmx_fragment_request, is_htmx_history_restore_request
from core.services.statsig import detect_device_type, log_event

# Rangos oficiales Cloudflare — mayo 2025
CF_RANGES: Final[tuple[str, ...]] = (
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
)

CF_NETS: Final[tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]] = tuple(map(ipaddress.ip_network, CF_RANGES))

logger = logging.getLogger(__name__)


def _is_cloudflare_addr(addr: str) -> bool:
    try:
        ip = ipaddress.ip_address(addr)
        return any(ip in net for net in CF_NETS)
    except ValueError:
        return False


class CloudflareRealIPMiddleware:
    """
    Reemplaza REMOTE_ADDR con CF-Connecting-IP **solo** si la petición
    proviene de un rango de Cloudflare. Además expone la IP en request.ip
    para usarla fácilmente en tus logs.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        cf_ip = request.headers.get("CF-Connecting-IP")
        proxy_ip = request.META.get("REMOTE_ADDR")

        if cf_ip and proxy_ip and _is_cloudflare_addr(proxy_ip):
            if _is_cloudflare_addr(cf_ip):
                logger.debug("CF-Connecting-IP (%s) también pertenece a rango CF; usando REMOTE_ADDR", cf_ip)
            else:
                # Sobrescribimos REMOTE_ADDR para que cualquier código downstream lo vea
                request.META["REMOTE_ADDR"] = cf_ip
                logger.debug("REMOTE_ADDR sustituido por CF-Connecting-IP %s", cf_ip)

        request_with_ip = cast(Any, request)
        request_with_ip.ip = cf_ip or request.META.get("REMOTE_ADDR")

        return self.get_response(request)


class CurrentViewMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        resolver = getattr(request, "resolver_match", None)
        if resolver and resolver.url_name:
            response["X-Current-View"] = resolver.url_name
        return response


class StatsigAnalyticsMiddleware:
    _SKIP_PATH_PREFIXES: Final[tuple[str, ...]] = ("/static/", "/media/")

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        self._track_request(request, response)
        return response

    def _track_request(self, request: HttpRequest, response: HttpResponse) -> None:
        if request.method != "GET" or response.status_code != 200:
            return

        if is_htmx_history_restore_request(request):
            return

        if request.path.startswith(self._SKIP_PATH_PREFIXES):
            return

        resolver = getattr(request, "resolver_match", None)
        if resolver is None or not resolver.url_name:
            return

        user_agent = request.headers.get("user-agent", "")
        metadata = {
            "url_name": resolver.url_name,
            "view_name": resolver.view_name or "",
            "path": request.path,
            "htmx": str(is_htmx_fragment_request(request)).lower(),
            "device_type": detect_device_type(user_agent),
            "locale": getattr(request, "LANGUAGE_CODE", "") or "",
            **{key: str(value) for key, value in resolver.kwargs.items()},
        }

        log_event(request, "page_view", metadata=metadata)

        user = getattr(request, "user", None)
        if request.path.startswith("/admin/") and getattr(user, "is_staff", False):
            log_event(
                request,
                "admin_page_view",
                metadata={
                    "path": request.path,
                    "view_name": resolver.view_name or "",
                    "url_name": resolver.url_name,
                },
            )
