import json

import logfire
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic.base import RedirectView

from blog.models import Post
from blog.services.chatgpt import improve_blog_post
from core.services.pretty import highlight_json


def handler404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Custom 404 handler."""
    logfire.warning("Page not found {path}", path=request.path)
    return render(request, "core/404.html", status=404)


def handler500(request: HttpRequest) -> HttpResponse:
    """Custom 500 handler."""
    logfire.exception("Internal server error at {path}", path=request.path)
    return render(request, "core/500.html", status=500)


def language_dropdown(request: HttpRequest) -> HttpResponse:
    return render(request, "core/language_dropdown.html")


@login_required
def chatgpt_improve_post(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        post = Post.objects.get(pk=post_id)
        improve_blog_post(post)
        post.refresh_from_db()

        if post.suggestions:
            response = json.dumps(post.suggestions, ensure_ascii=False, sort_keys=True, indent=2)
            formatted_response = highlight_json(response)
            return HttpResponse(formatted_response, content_type="text/html")
        else:
            return HttpResponse(status=204)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    except Exception:
        logfire.exception("Error improving post")
        return HttpResponse("An internal error occurred.", status=500, content_type="text/html")


class MediaView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args: list[str | None], **kwargs: dict[str, str]) -> str | None:
        self.url = f"https://media.eduzen.com.ar/{kwargs['path']}"
        logfire.warning("url redirected {url}", url=self.url)
        return super().get_redirect_url(*args, **kwargs)


class StaticView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args: list[str | None], **kwargs: dict) -> str | None:
        self.url = f"https://static.eduzen.com.ar/{kwargs['path']}"
        logfire.warning("url redirected {url}", url=self.url)
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
