from django.http import HttpRequest


def is_htmx_request(request: HttpRequest) -> bool:
    return bool(getattr(request, "htmx", False))


def is_htmx_history_restore_request(request: HttpRequest) -> bool:
    htmx = getattr(request, "htmx", None)
    return bool(getattr(htmx, "history_restore_request", False))


def is_htmx_fragment_request(request: HttpRequest) -> bool:
    return is_htmx_request(request) and not is_htmx_history_restore_request(request)
