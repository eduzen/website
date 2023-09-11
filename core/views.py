import logging
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.generic.base import RedirectView
from blog.models import Post
from blog.services.chatgpt import improve_blog_post
from core.services.pretty import highlight_json

logger = logging.getLogger(__name__)


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
            return JsonResponse({"message": "No suggestions found!"}, status=200)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", content_type="text/html")
    except Exception as e:
        logger.exception("Error improving post")
        return HttpResponse(str(e), content_type="text/html")


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
