from unittest.mock import patch

import pytest

from blog.models import Post
from blog.tasks import improve_blog_post_task
from blog.tests.factories import PostFactory


@pytest.mark.django_db
def test_improve_blog_post_task_fetches_and_improves_post() -> None:
    post = PostFactory.create()

    with patch("blog.tasks.improve_blog_post") as mock_improve:
        improve_blog_post_task(post.pk)

    mock_improve.assert_called_once()
    improved_post = mock_improve.call_args.args[0]
    assert improved_post.pk == post.pk


@pytest.mark.django_db
def test_improve_blog_post_task_raises_for_missing_post() -> None:
    with pytest.raises(Post.DoesNotExist):
        improve_blog_post_task(999999)
