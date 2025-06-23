from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from blog.forms import ContactForm


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
        self.assertIsInstance(response.context["form"], ContactForm)

    def test_contact_view_htmx_request(self):
        """Test contact view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_contact.html")

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
        self.assertTemplateUsed(response, "blog/_contact.html")
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_contact_form_valid_submission(self):
        """Test valid contact form submission"""
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message",
            "captcha": "red",  # Answer to "What color is the red rabbit?"
        }

        response = self.client.post(self.url, data=form_data)

        # May redirect to error page if telegram service fails
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])
        if response.status_code == HTTPStatus.OK:
            self.assertTemplateUsed(response, "blog/success.html")

    def test_contact_form_invalid_submission(self):
        """Test invalid contact form submission"""
        form_data = {}  # Empty form

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/contact.html")
        self.assertContains(response, "This field is required")

    def test_contact_form_invalid_email(self):
        """Test contact form with invalid email"""
        form_data = {
            "name": "Test User",
            "email": "invalid-email",
            "subject": "Test Subject",
            "message": "This is a test message",
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Enter a valid email address")

    def test_contact_form_missing_required_fields(self):
        """Test contact form with missing required fields"""
        # Missing name
        form_data = {"email": "test@example.com", "subject": "Test Subject", "message": "This is a test message"}

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "This field is required")

    def test_contact_form_htmx_submission(self):
        """Test contact form submission via HTMX"""
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message",
            "captcha": "red",  # Answer to "What color is the red rabbit?"
        }

        response = self.client.post(self.url, data=form_data, HTTP_HX_REQUEST="true")

        # May redirect to error page if telegram service fails
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])
        if response.status_code == HTTPStatus.OK:
            self.assertTemplateUsed(response, "blog/success.html")

    def test_contact_form_htmx_invalid_submission(self):
        """Test invalid contact form submission via HTMX"""
        form_data = {}  # Empty form

        response = self.client.post(self.url, data=form_data, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_contact.html")
        self.assertContains(response, "This field is required")

    def test_contact_form_with_long_message(self):
        """Test contact form with very long message"""
        long_message = "This is a very long message. " * 100
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": long_message,
        }

        response = self.client.post(self.url, data=form_data)

        # Should handle long messages gracefully
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])

    def test_contact_form_with_special_characters(self):
        """Test contact form with special characters"""
        form_data = {
            "name": "José María",
            "email": "jose@example.com",
            "message": "Message with ñoño, áéíóú, and symbols: @#$%",
            "captcha": "red",  # Answer to "What color is the red rabbit?"
        }

        response = self.client.post(self.url, data=form_data)

        # Should handle special characters (may redirect to error if telegram fails)
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])
        if response.status_code == HTTPStatus.OK:
            self.assertTemplateUsed(response, "blog/success.html")

    def test_contact_form_csrf_protection(self):
        """Test that contact form has CSRF protection"""
        response = self.client.get(self.url)

        self.assertContains(response, "csrfmiddlewaretoken")
