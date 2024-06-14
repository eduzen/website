import factory
from django.core.management.base import BaseCommand
from django.db.models.signals import pre_save

from blog.models import Post
from blog.services.parsers import apply_styles


class Command(BaseCommand):
    help = "Update old content to use new styles with BeautifulSoup"

    @factory.django.mute_signals(pre_save)
    def handle(self, *args: tuple[str], **options: dict[str, str]) -> None:
        # Fetch all records
        records = Post.objects.all()

        for record in records:
            # Apply styles using helper function
            styled_content = apply_styles(record.text)

            # Save the updated content
            record.text = styled_content
            record.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated content styles using BeautifulSoup!"))
