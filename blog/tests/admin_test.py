import pytest
from django.urls import reverse

from .factories import PostFactory, TagFactory


@pytest.fixture(scope="session")
def post(db):
    tags = TagFactory.create_batch(3)
    post = PostFactory.create()
    post.tags.set(tags)


@pytest.mark.parametrize(
    "url",
    (
        "admin:blog_post_changelist",
        "admin:blog_post_add",
    ),
)
def test_blog_admin(admin_client, url):
    response = admin_client.get(reverse(url))
    assert response.status_code == 200


@pytest.mark.parametrize("url", ("admin:blog_post_change", "admin:blog_post_delete"))
@pytest.mark.django_db
def test_blog_post_admin(admin_client, url):
    post = PostFactory.create()
    response = admin_client.get(reverse(url, args=(post.pk,)))
    assert response.status_code == 200
