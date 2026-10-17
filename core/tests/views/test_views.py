from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from blog.tests.factories import PostFactory
from core import views


@pytest.mark.parametrize("url", ("media/test.jpg", "media"))
def test_media_view_not_found(client, url):
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_media_view_redirects_to_external_host(client):
    response = client.get("/media/test.jpg")

    assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
    assert response["Location"] == "https://media.eduzen.com.ar/test.jpg"


def test_static_view_redirect_url_building():
    view = views.StaticView()
    view.request = RequestFactory().get("/")

    redirect_url = view.get_redirect_url(path="assets/app.js")

    assert redirect_url == "https://static.eduzen.com.ar/assets/app.js"


class FaviconTests(TestCase):
    def test_get(self):
        response = self.client.get("/favicon.ico")

        assert response.status_code == HTTPStatus.OK
        assert response["Cache-Control"] == "max-age=31536000, immutable, public"
        assert response["Content-Type"] == "image/svg+xml"
        assert response.content.startswith(b"<svg")


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

    def test_version_view_json_response(self):
        response = self.client.get("/version/?format=json")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["Content-Type"], "application/json")
        payload = response.json()
        self.assertIn("version", payload)
        self.assertIn("build_date", payload)

    def test_version_view_html_response(self):
        response = self.client.get("/version/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "core/version.html")
        self.assertContains(response, "<table", html=False)
        self.assertContains(response, "Version")
        self.assertContains(response, "Build Date")

    def test_version_view_htmx_response(self):
        response = self.client.get("/version/", headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<table", html=False)
        self.assertNotContains(response, "<!DOCTYPE html>")
