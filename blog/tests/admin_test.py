import pytest
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from http import HTTPStatus
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
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("url", ("admin:blog_post_change", "admin:blog_post_delete"))
@pytest.mark.django_db
def test_blog_post_admin(admin_client, url):
    post = PostFactory.create()
    response = admin_client.get(reverse(url, args=(post.pk,)))
    assert response.status_code == HTTPStatus.OK


class SessionAdminTest(TestCase):
    def setUp(self):
        # Create a superuser and log in for admin access
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="testuser", password="testpass", email="test@example.com"
        )
        self.client.login(username="testuser", password="testpass")

    def test_list_display_custom_fields(self):
        # Access the admin page for sessions
        response = self.client.get(reverse("admin:sessions_session_changelist"))
        self.assertContains(response, "session_key")
        self.assertContains(response, "_session_data")
        self.assertContains(response, "expire_date")
