from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class TestClassesView(TestCase):
    """Test ClassesView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("classes")
        cache.clear()

    def test_classes_view_get(self):
        """Test GET request to classes view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/classes.html")

    def test_classes_view_htmx_request(self):
        """Test classes view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_classes.html")

    def test_classes_view_regular_request(self):
        """Test classes view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/classes.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_classes_view_htmx_request_no_doctype(self):
        """Test classes view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_classes.html")
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_classes_view_post_request(self):
        """Test POST request to classes view (should handle gracefully)"""
        response = self.client.post(self.url, data={})
        # Should handle POST gracefully or return method not allowed
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])
