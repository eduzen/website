import pytest

from blog.tests.factories import PostFactory, TagFactory


@pytest.fixture(scope="session")
def post(db):
    tags = TagFactory.create_batch(3)
    post = PostFactory.create()
    post.tags.set(tags)
