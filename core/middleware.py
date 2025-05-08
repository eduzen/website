import ipaddress
import logging
from collections.abc import Callable

# Add type annotations for custom request attribute
from typing import TYPE_CHECKING, Final

from django.http import HttpRequest, HttpResponse

if TYPE_CHECKING:

    class CustomHttpRequest(HttpRequest):
        ip: str | None


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
    Reemplaza REMOTE_ADDR con CF‑Connecting‑IP **solo** si la petición
    proviene de un rango de Cloudflare. Además expone la IP en request.ip
    para usarla fácilmente en tus logs.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: "CustomHttpRequest") -> HttpResponse:
        cf_ip = request.headers.get("CF-Connecting-IP")
        proxy_ip = request.META.get("REMOTE_ADDR")

        if cf_ip and proxy_ip and _is_cloudflare_addr(proxy_ip):
            if _is_cloudflare_addr(cf_ip):
                logger.debug("CF-Connecting-IP (%s) también pertenece a rango CF; usando REMOTE_ADDR", cf_ip)
            else:
                # Sobrescribimos REMOTE_ADDR para que cualquier código downstream lo vea
                request.META["REMOTE_ADDR"] = cf_ip
                logger.debug("REMOTE_ADDR sustituido por CF-Connecting-IP %s", cf_ip)

        # atributo de conveniencia
        request.ip = request.META.get("REMOTE_ADDR")

        return self.get_response(request)
