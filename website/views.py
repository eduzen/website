import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import translation
from django.views.generic.base import RedirectView

logger = logging.getLogger("website.views")

favicon_view = RedirectView.as_view(url="https://static.eduzen.com.ar/blog/img/favicon.ico", permanent=True)


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


def set_language(request: HttpRequest, language_code: str) -> HttpResponse:
    if translation.check_for_language(language_code):
        translation.activate(language_code)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language_code
    return redirect(request.headers.get("referer"))
