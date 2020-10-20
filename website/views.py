import logging

from django.views.generic.base import RedirectView

logger = logging.getLogger("website.views")

favicon_view = RedirectView.as_view(url="https://static.eduzen.com.ar/blog/img/favicon.ico", permanent=True)


class MediaView(RedirectView):
    is_permanent = True

    def get_redirect_url(self, *args, **kwargs):
        self.url = f"https://media.eduzen.com.ar/{kwargs['path']}"
        logger.warn("url redirected %s", (self.url,))
        return super().get_redirect_url(*args, **kwargs)


class StaticView(RedirectView):
    is_permanent = True

    def get_redirect_url(self, *args, **kwargs):
        self.url = f"https://static.eduzen.com.ar/{kwargs['path']}"
        logger.warn("url redirected %s", (self.url,))
        return super().get_redirect_url(*args, **kwargs)
