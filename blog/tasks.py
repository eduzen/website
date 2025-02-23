# blog/tasks.py
from django.db import transaction

from blog.models import Post
from blog.services.chatgpt import improve_blog_post


def improve_blog_post_task(post_id: int) -> None:
    """
    A Celery task that fetches a Post by ID and improves it using ChatGPT (pydantic-ai).
    """
    with transaction.atomic():
        post = Post.objects.select_for_update().get(pk=post_id)
        improve_blog_post(post)
