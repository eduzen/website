from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class TestSuccessView(TestCase):
    """Test SuccessView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("success")
        cache.clear()

    def test_success_view_get(self):
        """Test GET request to success view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/success.html")

    def test_success_view_htmx_request(self):
        """Test success view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Success view doesn't have separate HTMX template, uses same template
        self.assertTemplateUsed(response, "blog/success.html")

    def test_success_view_regular_request(self):
        """Test success view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/success.html")
        # Success page is a simple template without full HTML structure
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_success_view_htmx_request_no_doctype(self):
        """Test success view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/success.html")
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_success_view_post_request(self):
        """Test POST request to success view (should handle gracefully)"""
        response = self.client.post(self.url, data={})
        # Should handle POST gracefully or return method not allowed
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])

    def test_success_view_content(self):
        """Test success view contains expected content"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Check for actual content in the success template
        self.assertContains(response, "Thank you for your message")

    def test_success_view_navigation_links(self):
        """Test success view has navigation links"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Success pages typically have links back to home or contact
        self.assertTrue(
            "home" in response.content.decode().lower()
            or "contact" in response.content.decode().lower()
            or "back" in response.content.decode().lower()
        )
