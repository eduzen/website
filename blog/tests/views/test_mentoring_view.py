from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class TestMentoringView(TestCase):
    """Test MentoringView functionality"""

    def setUp(self) -> None:
        activate("en")
        self.url = reverse("mentoring")
        cache.clear()

    def test_mentoring_view_get(self) -> None:
        """Test GET request to mentoring view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/mentoring.html")

    def test_mentoring_view_htmx_request(self) -> None:
        """Test mentoring view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Mentoring")

    def test_mentoring_view_regular_request(self) -> None:
        """Test mentoring view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/mentoring.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_mentoring_view_htmx_request_no_doctype(self) -> None:
        """Test mentoring view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Mentoring")

    def test_mentoring_view_content_sections(self) -> None:
        """Test mentoring page has all key sections"""
        response = self.client.get(self.url)

        self.assertContains(response, "Mentoring")
        self.assertContains(response, "Code Review")
        self.assertContains(response, "Career Navigation")
        self.assertContains(response, "Pair Programming")
        self.assertContains(response, "How it works")
        self.assertContains(response, "Who is this for")

    def test_mentoring_view_post_request(self) -> None:
        """Test POST request to mentoring view (should handle gracefully)"""
        response = self.client.post(self.url, data={})
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])
