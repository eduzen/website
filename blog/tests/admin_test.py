import pytest
from django.urls import reverse

from .factories import PostFactory


@pytest.fixture(scope="session")
def post(db):
    PostFactory.create()


def test_root_admin(admin_client):
    response = admin_client.get(reverse("admin:index"))
    assert response.status_code == 200


@pytest.mark.parametrize("app", ("blog", "expenses", "snippets", "files", "robots", "constance"))
def test_admin(admin_client, app):
    response = admin_client.get(reverse("admin:app_list", kwargs={"app_label": app}))
    assert response.status_code == 200


@pytest.mark.parametrize("url", ("admin:blog_post_changelist", "admin:blog_post_add", "admin:blog_post_autocomplete"))
def test_blog_admin(admin_client, url):
    response = admin_client.get(reverse(url))
    assert response.status_code == 200


@pytest.mark.parametrize("url", ("admin:blog_post_change", "admin:blog_post_delete"))
@pytest.mark.django_db
def test_blog_post_admin(admin_client, url):
    post = PostFactory.create()
    response = admin_client.get(reverse(url, args=(post.pk,)))
    assert response.status_code == 200
