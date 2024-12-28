from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import Post

fake = Faker()


class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **options):
        # Create dummy users
        for _ in range(10):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            User.objects.create_user(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS("Successfully created dummy users!"))

        # Add more code here to populate other models with dummy data
        # Create dummy posts
        for _ in range(10):
            title = fake.sentence()
            text = fake.paragraph()
            summary = fake.paragraph()
            slug = fake.slug()
            author = User.objects.first()
            published_date = fake.date_time_this_year()
            Post.objects.create(
                slug=slug, published_date=published_date, title=title, text=text, author=author, summary=summary
            )

        self.stdout.write(self.style.SUCCESS("Successfully created dummy posts!"))
