import logging

from django.http import HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic.base import RedirectView

logger = logging.getLogger("website.views")


class MediaView(RedirectView):
    is_permanent = True

    def get_redirect_url(self, *args: list[str | None], **kwargs: dict[str, str]) -> str | None:
        self.url = f"https://media.eduzen.com.ar/{kwargs['path']}"
        logger.warn("url redirected %s", (self.url,))
        return super().get_redirect_url(*args, **kwargs)


class StaticView(RedirectView):
    is_permanent = True

    def get_redirect_url(self, *args: list[str | None], **kwargs: dict) -> str | None:
        self.url = f"https://static.eduzen.com.ar/{kwargs['path']}"
        logger.warn("url redirected %s", (self.url,))
        return super().get_redirect_url(*args, **kwargs)


@require_GET
@cache_control(max_age=60 * 60 * 24 * 365, immutable=True, public=True)  # one year
def favicon_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + '<text y=".9em" font-size="90">🤓</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )
