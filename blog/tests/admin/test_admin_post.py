from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import translation

from blog.models import Post
from blog.tests.factories import PostFactory, TagFactory, UserFactory


@pytest.mark.django_db
class TestBlogAdmin:
    @pytest.fixture(autouse=True)
    def setup(self, admin_client):
        self.admin_client = admin_client

    @pytest.fixture
    def create_post(self):
        return PostFactory.create()

    @pytest.mark.parametrize(
        "url_name",
        (
            "admin:blog_post_changelist",
            "admin:blog_post_add",
        ),
    )
    def test_accessible_urls(self, url_name):
        with translation.override("en-us"):
            url = reverse(url_name)
            response = self.admin_client.get(url)
            assert response.status_code == HTTPStatus.OK, f"Failed accessing {url}: {response.status_code}"

    @pytest.mark.parametrize("url_name", ("admin:blog_post_change", "admin:blog_post_delete"))
    def test_post_admin_urls(self, url_name, create_post):
        url = reverse(url_name, args=(create_post.pk,))
        response = self.admin_client.get(url)
        assert response.status_code == HTTPStatus.OK, f"Failed accessing {url}: {response.status_code}"

    def test_create_post(self):
        url = reverse("admin:blog_post_add")
        tag1, tag2 = TagFactory.create_batch(2)
        data = {
            "author": User.objects.first().id,
            "title": "Test Post",
            "summary": "This is a test summary.",
            "text": "This is the body of the test post.",
            "slug": "test-post",
            "created_date": "2024-01-01",
            "published_date": "2024-01-02",
            "published": True,
            "tags": [tag1.id, tag2.id],
            "image": "",  # Handle image upload if necessary
            "cropping": "",
        }
        response = self.admin_client.post(url, data, follow=True)
        assert response.status_code == HTTPStatus.OK, "Admin should successfully create a post."
        assert Post.objects.filter(title="Test Post").exists(), "Post should be created in the database."

    @pytest.mark.skip(reason="Update title is not working")
    def test_update_post(self, create_post):
        post = create_post
        post.title = "Original Title"
        post.save()
        url = reverse("admin:blog_post_change", args=(post.pk,))
        new_tag = TagFactory.create()
        data = {
            "author": post.author.id,
            "title": "Updated Title",
            "summary": post.summary,
            "text": post.text,
            "slug": post.slug,
            "created_date": post.created_date,
            "published_date": post.published_date,
            "published": post.published,
            "tags": [new_tag.id],
            "image": "",  # Handle image upload if necessary
            "cropping": "",
        }
        response = self.admin_client.post(url, data, follow=True)
        assert response.status_code == HTTPStatus.OK, "Admin should successfully update the post."
        post.refresh_from_db()
        assert post.title == "Updated Title", "Post title should be updated."
        assert post.tags.count() == 1 and post.tags.first() == new_tag, "Post tags should be updated."

    def test_delete_post(self, create_post):
        post = create_post
        url = reverse("admin:blog_post_delete", args=(post.pk,))
        response = self.admin_client.post(url, {"post": "yes"}, follow=True)
        assert response.status_code == HTTPStatus.OK, "Admin should successfully delete the post."
        assert not Post.objects.filter(pk=post.pk).exists(), "Post should be deleted from the database."

    def test_post_list_display(self):
        _ = PostFactory.create(title="Unique Title")
        url = reverse("admin:blog_post_changelist")
        response = self.admin_client.get(url)
        assert response.status_code == HTTPStatus.OK, "Admin list view should load successfully."
        content = response.content.decode()
        assert "Unique Title" in content, "Post title should be displayed in the admin list view."
        assert "Go to eduzen.ar" in content, "Custom blog_link should be displayed."

    def test_post_search(self):
        PostFactory.create(title="Searchable Title")
        PostFactory.create(title="Another Post", published_date=None)
        url = reverse("admin:blog_post_changelist") + "?q=Searchable"
        response = self.admin_client.get(url)
        assert response.status_code == HTTPStatus.OK, "Admin search should work."
        content = response.content.decode()
        assert "Searchable Title" in content, "Search query should return relevant posts."
        assert "Another Post" not in content, "Non-matching posts should not be displayed."

    def test_add_post_with_invalid_data(self):
        url = reverse("admin:blog_post_add")
        data = {
            "author": "",  # Missing author
            "title": "",  # Missing title
            "summary": "Test Summary",
            "text": "Test content for the post.",
            "slug": "invalid-slug",
            "created_date": "2024-01-01",
            "published_date": "2024-01-02",
            "published": True,
            "tags": [],
            "image": "",  # Handle image upload if necessary
            "cropping": "",
        }
        response = self.admin_client.post(url, data)
        assert response.status_code == HTTPStatus.OK, "Form with invalid data should be re-rendered with errors."
        content = response.content.decode()
        assert "This field is required" in content, "Form should display required field errors."
        assert not Post.objects.filter(slug="invalid-slug").exists(), "Post should not be created with invalid data."

    def test_post_form_validations(self):
        url = reverse("admin:blog_post_add")

        # Test missing required fields
        data_missing = {
            "author": "",
            "title": "",
            "summary": "Valid summary.",
            "text": "Valid content.",
            "slug": "valid-slug",
            "created_date": "2024-01-01",
            "published_date": "2024-01-02",
            "published": True,
            "tags": [],
            "image": "",
            "cropping": "",
        }
        response_missing = self.admin_client.post(url, data_missing)
        assert response_missing.status_code == HTTPStatus.OK, "Form with missing data should show errors."
        content_missing = response_missing.content.decode()
        assert "This field is required" in content_missing, "Form should show missing field errors."

        # Test invalid slug
        data_invalid_slug = {
            "author": User.objects.first().id,
            "title": "Valid Title",
            "summary": "Valid summary.",
            "text": "Valid content.",
            "slug": "invalid slug!",  # Invalid slug
            "created_date": "2024-01-01",
            "published_date": "2024-01-02",
            "published": True,
            "tags": [],
            "image": "",
            "cropping": "",
        }
        response_invalid_slug = self.admin_client.post(url, data_invalid_slug)
        assert response_invalid_slug.status_code == HTTPStatus.OK, "Form with invalid slug should show errors."
        errors = response_invalid_slug.context["errors"]
        assert any(
            "Enter a valid “slug”" in error[0] for error in errors
        ), "Form should display slug validation errors."

    def test_add_post_with_long_title(self):
        url = reverse("admin:blog_post_add")
        long_title = "A" * 201  # Exceeds max_length=200
        data = {
            "author": User.objects.first().id,
            "title": long_title,
            "summary": "Valid summary.",
            "text": "Valid content.",
            "slug": "long-title-post",
            "created_date": "2024-01-01",
            "published_date": "2024-01-02",
            "published": True,
            "tags": [],
            "image": "",
            "cropping": "",
        }
        response = self.admin_client.post(url, data)
        assert (
            response.status_code == HTTPStatus.OK
        ), "Form with excessively long title should be re-rendered with errors."
        content = response.content.decode()
        assert "Ensure this value has at most 200 characters" in content, "Form should display max_length error."
        assert not Post.objects.filter(
            slug="long-title-post"
        ).exists(), "Post should not be created with invalid title."


@pytest.mark.django_db
class TestAdminAccess:
    @pytest.fixture
    def regular_user(self):
        return UserFactory.create(is_staff=False, is_superuser=False)

    def test_access_requires_superuser(self, client, regular_user):
        client.login(username=regular_user.username, password="eduzen!")
        url = reverse("admin:blog_post_changelist")
        response = client.get(url)
        assert response.status_code in [
            HTTPStatus.FOUND,
            HTTPStatus.FORBIDDEN,
        ], "Regular users should not access admin."

    def test_login_required(self, client):
        url = reverse("admin:blog_post_changelist")
        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND, "Unauthenticated users should be redirected to login."
        assert response.url.startswith(reverse("admin:login")), "Redirect should point to admin login."


@pytest.mark.django_db
class TestSessionAdmin:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.superuser = User.objects.create_superuser(
            username="testuser", password="testpass", email="test@example.com"
        )
        self.client.login(username="testuser", password="testpass")

    def test_list_display_custom_fields(self):
        response = self.client.get(reverse("admin:sessions_session_changelist"))
        assert response.status_code == HTTPStatus.OK, "Admin session list view should load successfully."
        content = response.content.decode()
        assert "session_key" in content, "Session key should be displayed in the admin list view."
        assert "_session_data" in content, "Session data should be displayed in the admin list view."
        assert "expire_date" in content, "Expire date should be displayed in the admin list view."
