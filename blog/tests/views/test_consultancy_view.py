from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class TestConsultancyView(TestCase):
    """Test ConsultancyView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("consultancy")
        cache.clear()

    def test_consultancy_view_get(self):
        """Test GET request to consultancy view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/consultancy.html")

    def test_consultancy_view_htmx_request(self):
        """Test consultancy view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render the partial content only
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Consultancy Services")

    def test_consultancy_view_regular_request(self):
        """Test consultancy view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/consultancy.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_consultancy_view_htmx_request_no_doctype(self):
        """Test consultancy view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Consultancy Services")

    def test_consultancy_view_post_request(self):
        """Test POST request to consultancy view (should handle gracefully)"""
        response = self.client.post(self.url, data={})
        # Should handle POST gracefully or return method not allowed
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])
