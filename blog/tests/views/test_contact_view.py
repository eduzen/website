from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class TestContactView(TestCase):
    """Test ContactView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("contact")
        cache.clear()

    def test_contact_view_get(self):
        """Test GET request to contact view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/contact.html")
        self.assertNotIn("form", response.context)
        self.assertNotContains(response, 'hx-post="/en/contact/"')
        for text in (
            "Let's connect",
            "me@eduzen.com.ar",
            "LinkedIn",
            "GitHub",
            "Telegram",
            "@eduzen",
            "Based in Amsterdam, but always happy to collaborate across time zones.",
        ):
            self.assertContains(response, text)

    def test_contact_view_htmx_request(self):
        """Test contact view with HTMX request"""
        response = self.client.get(self.url, headers={"hx-request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render the partial content only
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Let's connect")

    def test_contact_view_regular_request(self):
        """Test contact view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/contact.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_contact_view_htmx_request_no_doctype(self):
        """Test contact view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Let's connect")

    def test_contact_view_htmx_history_restore_gets_full_page(self):
        response = self.client.get(
            self.url,
            headers={"HX-Request": "true", "HX-History-Restore-Request": "true"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<!DOCTYPE html>", count=1)
        self.assertContains(response, 'id="main-navbar"', count=1)
        self.assertContains(response, 'id="content"', count=1)
        self.assertContains(response, "Let's connect")

    def test_contact_rejects_form_submissions(self):
        response = self.client.post(self.url, data={"message": "Hello"})

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
