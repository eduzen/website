# type: ignore
from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from blog.tests.factories import PostFactory


@pytest.mark.parametrize("url", ("media/test.jpg", "media"))
def test_media_view_not_found(client, url):
    response = client.get(url)
    assert response.status_code == 404


class FaviconTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/favicon.ico")

        assert response.status_code == HTTPStatus.OK
        assert response["Cache-Control"] == "max-age=31536000, immutable, public"
        assert response["Content-Type"] == "image/svg+xml"
        assert response.content.startswith(b"<svg")


class LanguageDropdownViewTest(SimpleTestCase):
    def test_language_dropdown_renders_correct_template(self):
        # Use the reverse() function to get the URL of the view.
        # Assuming the name of the URL pattern for this view is 'language_dropdown'
        response = self.client.get(reverse("language_dropdown"))

        assert response.status_code == HTTPStatus.OK
        # Check that the correct template is used
        self.assertTemplateUsed(response, "core/language_dropdown.html")


class ChatGPTImprovePostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = PostFactory.create()
        self.url = reverse("chatgpt_improve_post", args=[self.post.pk])

    def test_user_not_logged_in(self):
        response = self.client.get(self.url)
        assert response.status_code == HTTPStatus.FOUND  # Should redirect to login page

    @patch("core.views.improve_blog_post")
    def test_post_not_found(self, mock_improve):
        self.client.login(username="testuser", password="12345")
        wrong_post_id_url = reverse("chatgpt_improve_post", args=[9999])
        response = self.client.get(wrong_post_id_url)

        assert response.status_code == HTTPStatus.OK
        assert response.content.decode() == "Post not found"
        mock_improve.assert_not_called()  # Since the post doesn't exist, improve_blog_post shouldn't be called

    @patch("core.views.improve_blog_post")
    def test_post_with_suggestions(self, mock_improve):
        mock_improve.return_value = None  # Assume this function returns None after modifying the post
        self.post.suggestions = {"suggestion": "Improved Title"}
        self.post.save()

        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        assert "Improved Title" in response.content.decode()
        mock_improve.assert_called_once()  # Ensure the function was called

    @patch("core.views.improve_blog_post")
    def test_post_without_suggestions(self, mock_improve):
        mock_improve.return_value = None
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)

        assert response.json() == {"message": "No suggestions found!"}
        mock_improve.assert_called_once()
