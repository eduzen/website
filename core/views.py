import logging
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from blog.models import Post
from blog.services.chatgpt import improve_blog_post

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
            response = json.dumps(post.suggestions, sort_keys=True, indent=2)
            formatter = HtmlFormatter(style="colorful")
            response = highlight(response, JsonLexer(), formatter)
            data = f"<style>{formatter.get_style_defs()}</style><br>{response}"
            return HttpResponse(data, content_type="text/html")
        else:
            return JsonResponse({"message": "No suggestions found!"}, status=200)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", content_type="text/html")
    except Exception as e:
        logger.exception("Error improving post")
        return HttpResponse(str(e), content_type="text/html")
