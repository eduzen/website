# blog/management/commands/improve_posts.py
from django.core.management.base import BaseCommand

from blog.models import Post
from blog.tasks import improve_blog_post_task


class Command(BaseCommand):
    help = "Improve all blog posts using pydantic-ai and store suggestions in the DB."

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            # If you want async using Celery:
            improve_blog_post_task(post.pk)

            # If you just want direct synchronous calls (no queue):
            # improve_blog_post_task(post.pk)  # but remove @shared_task or call a direct function

            self.stdout.write(
                self.style.SUCCESS(f"Queued improvement for post {post.pk} (title: {post.title[:50]}...)")
            )
