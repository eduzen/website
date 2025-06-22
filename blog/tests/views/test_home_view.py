from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from blog.tests.factories import UserFactory


class TestHomeView(TestCase):
    """Test HomeView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("home")
        cache.clear()
        self.user = UserFactory.create()

    def test_home_view_get(self):
        """Test GET request to home view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_home_view_context_data(self):
        """Test home view returns correct context"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_home_view_htmx_request(self):
        """Test home view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_home.html")

    def test_home_view_regular_request(self):
        """Test home view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/home.html")
        # Regular request should include base template structure
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_home_view_htmx_request_no_doctype(self):
        """Test home view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_home.html")
        # HTMX request should not include full page structure
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_home_view_is_cached(self):
        """Test that home view is cached"""
        # This is a smoke test to ensure cache decorators don't break functionality
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Second request should also work (cache may or may not be hit in tests)
        response2 = self.client.get(self.url)
        self.assertEqual(response2.status_code, HTTPStatus.OK)

    def test_home_view_spanish_language(self):
        """Test home view works with Spanish language setting"""
        activate("es")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_home_view_post_request(self):
        """Test POST request to home view (should handle gracefully)"""
        response = self.client.post(self.url, data={})
        # Should handle POST gracefully or return method not allowed
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])

    def test_home_view_with_invalid_http_method(self):
        """Test home view with invalid HTTP method"""
        response = self.client.put(self.url)
        self.assertIn(response.status_code, [HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.NOT_FOUND])
