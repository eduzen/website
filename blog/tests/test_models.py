# blog/tests/models_test.py
import pytest
from django.utils import timezone

from .factories import PostFactory


@pytest.mark.django_db
def test_post_publish_method():
    post = PostFactory(published_date=None)
    assert not post.published, "Post should initially be unpublished."

    post.publish()
    assert post.published, "Post should be published after calling publish()."
    assert post.published_date is not None, "published_date should be set after publishing."


@pytest.mark.django_db
def test_post_published_property():
    post_published = PostFactory(published_date=timezone.now())
    post_unpublished = PostFactory(published_date=None)

    assert post_published.published is True, "Post with published_date should be marked as published."
    assert post_unpublished.published is False, "Post without published_date should not be marked as published."
