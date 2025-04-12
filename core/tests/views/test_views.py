from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from blog.tests.factories import PostFactory


@pytest.mark.parametrize("url", ("media/test.jpg", "media"))
def test_media_view_not_found(client, url):
    response = client.get(url)
    assert response.status_code == 404


class FaviconTests(TestCase):
    def test_get(self):
        response = self.client.get("/favicon.ico")

        assert response.status_code == HTTPStatus.OK
        assert response["Cache-Control"] == "max-age=31536000, immutable, public"
        assert response["Content-Type"] == "image/svg+xml"
        assert response.content.startswith(b"<svg")


class LanguageDropdownViewTest(TestCase):
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

        assert response.status_code == HTTPStatus.NOT_FOUND
        mock_improve.assert_not_called()

    @patch("core.views.improve_blog_post")
    def test_post_with_suggestions(self, mock_improve):
        # Set up post with suggestions
        self.post.suggestions = {"title": "Improved Title", "summary": "Better summary"}
        self.post.save()

        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)

        # Verify response
        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "Improved Title" in content
        assert "Better summary" in content
        mock_improve.assert_called_once_with(self.post)

    @patch("core.views.improve_blog_post")
    def test_post_without_suggestions(self, mock_improve):
        # Ensure post has no suggestions
        self.post.suggestions = None
        self.post.save()

        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)

        # Verify response is No Content
        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_improve.assert_called_once_with(self.post)

    @patch("core.views.improve_blog_post")
    def test_exception_handling(self, mock_improve):
        # Make the improve_blog_post function raise an exception
        mock_improve.side_effect = Exception("Test exception")

        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)

        # Verify response is Internal Server Error
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "An internal error occurred" in response.content.decode()
        mock_improve.assert_called_once_with(self.post)


class CoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_custom_404_page(self):
        """Test that a non-existent URL returns the custom 404 page."""
        response = self.client.get("/a-non-existent-url/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "core/404.html")
        self.assertContains(response, "404 - Page Not Found", status_code=404)
        self.assertContains(response, "Go back to Home", status_code=404)
