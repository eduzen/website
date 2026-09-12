from io import StringIO
from unittest.mock import Mock, call, patch

from django.core.management import call_command
from django.test import TestCase

from blog.tests.factories import PostFactory


class TestImprovePostsCommand(TestCase):
    @patch("blog.management.commands.improve_posts.improve_blog_post_task")
    def test_improve_posts_calls_task_for_each_post(self, mock_task: Mock) -> None:
        first_post = PostFactory.create(title="First post")
        second_post = PostFactory.create(title="Second post")

        out = StringIO()
        call_command("improve_posts", stdout=out)

        mock_task.assert_has_calls([call(first_post.pk), call(second_post.pk)], any_order=False)
        assert mock_task.call_count == 2

        output = out.getvalue()
        assert f"Queued improvement for post {first_post.pk}" in output
        assert f"Queued improvement for post {second_post.pk}" in output

    @patch("blog.management.commands.improve_posts.improve_blog_post_task")
    def test_improve_posts_with_no_posts(self, mock_task: Mock) -> None:
        out = StringIO()

        call_command("improve_posts", stdout=out)

        mock_task.assert_not_called()
        assert out.getvalue() == ""
