from django.core.management.base import BaseCommand

from blog.factories import TagFactory, PostFactory


class Command(BaseCommand):
    help = "Fills database."

    def handle(self, *args, **options):
        tags = TagFactory.create_batch(5)
        python_tag = TagFactory.create(word="python")
        for _ in range(10):
            post = PostFactory.create(tags=tags)
            print("post", post)
        for _ in range(5):
            post = PostFactory.create(tags=[python_tag])
            print("post", post)
        for _ in range(2):
            post = PostFactory.create(published_date=None, tags=[python_tag] + tags)
