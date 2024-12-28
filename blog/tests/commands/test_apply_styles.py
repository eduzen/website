from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from blog.services.parsers import apply_styles
from blog.tests.factories import PostFactory


class TestUpdateContentStylesCommand(TestCase):
    def test_update_styles(self):
        """Ensure that the management command updates each Post's text."""
        # 1. Create some Post objects
        original_text_1 = "Some <p>content</p>"
        original_text_2 = "<div>Another content</div>"

        post1 = PostFactory.create(text=original_text_1)
        post2 = PostFactory.create(text=original_text_2)

        # 2. Call the command and capture output
        out = StringIO()
        call_command("apply_styles", stdout=out)

        # 3. Refresh from DB
        post1.refresh_from_db()
        post2.refresh_from_db()

        # 4. Check that the command applied styles
        assert post1.text == apply_styles(original_text_1)
        assert post2.text == apply_styles(original_text_2)

        # 5. Optionally, verify the success message
        output = out.getvalue()
        assert "Successfully updated content styles" in output
