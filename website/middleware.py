from collections.abc import Callable
from django.http import HttpRequest, HttpResponse


class CloudflareMiddleware:
    """
    Middleware for correctly obtaining the client's IP address when the
    Django application is behind Cloudflare's proxy. When the application
    is behind Cloudflare's reverse proxy, the actual IP address of the client
    is stored in the 'CF-Connecting-IP' header. This middleware ensures that
    the application gets the correct client IP, either from the header added
    by Cloudflare or falls back to the default Django method.
    """

    def __init__(self, get_response: Callable) -> None:
        """
        Initialize the middleware with the given get_response callable.

        Args:
            get_response (callable): The next middleware or view to process the request.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request to set the correct client IP address.

        Args:
            request (HttpRequest): The incoming request object.

        Returns:
            HttpResponse: The response object after processing.
        """
        ip = request.headers.get("CF-Connecting-IP", request.META["REMOTE_ADDR"])
        request.ip = ip  # type: ignore
        return self.get_response(request)
