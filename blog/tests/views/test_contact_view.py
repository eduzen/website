from http import HTTPStatus
from unittest.mock import patch

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
        # With django-template-partials, HTMX requests render the partial content only
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Contact")

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
        self.assertContains(response, "Contact")

    @patch("blog.views.send_contact_message")
    def test_contact_form_valid_submission(self, mock_send_telegram):
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
        mock_send_telegram.assert_called_once_with(
            name="Test User", email="test@example.com", message="This is a test message"
        )

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
            "message": "This is a test message",
            "captcha": "red",
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Enter a valid email address")

    def test_contact_form_missing_required_fields(self):
        """Test contact form with missing required fields"""
        # Missing name
        form_data = {"email": "test@example.com", "message": "This is a test message", "captcha": "red"}

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "This field is required")

    @patch("blog.views.send_contact_message")
    def test_contact_form_htmx_submission(self, mock_send_telegram):
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

    @patch("blog.views.send_contact_message")
    def test_contact_form_htmx_invalid_submission(self, mock_send_telegram):
        """Test invalid contact form submission via HTMX"""
        form_data = {}  # Empty form

        response = self.client.post(self.url, data=form_data, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render the contact template
        self.assertTemplateUsed(response, "blog/contact.html")
        self.assertContains(response, "This field is required")
        mock_send_telegram.assert_not_called()

    @patch("blog.views.send_contact_message")
    def test_contact_form_with_long_message(self, mock_send_telegram):
        """Test contact form with very long message"""
        long_message = "This is a very long message. " * 100
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": long_message,
            "captcha": "red",  # Answer to "What color is the red rabbit?"
        }

        response = self.client.post(self.url, data=form_data)

        # Should handle long messages gracefully
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])
        mock_send_telegram.assert_called_once()
        call_args = mock_send_telegram.call_args
        self.assertEqual(call_args.kwargs["name"], "Test User")
        self.assertEqual(call_args.kwargs["email"], "test@example.com")
        # Just verify the message is long and starts correctly
        self.assertTrue(call_args.kwargs["message"].startswith("This is a very long message."))
        self.assertGreater(len(call_args.kwargs["message"]), 1000)  # Verify it's actually long

    @patch("blog.views.send_contact_message")
    def test_contact_form_with_special_characters(self, mock_send_telegram):
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

        mock_send_telegram.assert_called_once_with(
            name="José María", email="jose@example.com", message="Message with ñoño, áéíóú, and symbols: @#$%"
        )

    @patch("blog.views.send_contact_message")
    def test_contact_form_csrf_protection(self, mock_send_telegram):
        """Test that contact form has CSRF protection"""
        response = self.client.get(self.url)

        self.assertContains(response, "csrfmiddlewaretoken")
        mock_send_telegram.assert_not_called()

    @patch("blog.views.send_contact_message")
    def test_contact_form_successful_telegram_submission(self, mock_send_telegram):
        """Test contact form submission with successful Telegram message"""
        # Mock successful Telegram API response
        mock_send_telegram.return_value = {"ok": True, "result": {"message_id": 123}}

        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message",
            "captcha": "red",  # Answer to "What color is the red rabbit?"
        }

        response = self.client.post(self.url, data=form_data)

        # Should redirect to success page when Telegram API succeeds
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/success.html")

        # Verify Telegram service was called with correct data
        mock_send_telegram.assert_called_once_with(
            name="Test User", email="test@example.com", message="This is a test message"
        )

    @patch("blog.views.send_contact_message")
    def test_contact_form_telegram_failure_handling(self, mock_send_telegram):
        """Test contact form handles Telegram API failures gracefully"""
        # Mock Telegram API failure
        mock_send_telegram.side_effect = Exception("Telegram API error")

        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message",
            "captcha": "red",  # Answer to "What color is the red rabbit?"
        }

        response = self.client.post(self.url, data=form_data)

        # Should redirect to error page when Telegram fails
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Verify Telegram service was attempted
        mock_send_telegram.assert_called_once_with(
            name="Test User", email="test@example.com", message="This is a test message"
        )

    @patch("blog.views.send_contact_message")
    def test_contact_form_htmx_successful_telegram(self, mock_send_telegram):
        """Test contact form HTMX submission with successful Telegram message"""
        # Mock successful Telegram API response
        mock_send_telegram.return_value = {"ok": True, "result": {"message_id": 123}}

        form_data = {
            "name": "HTMX User",
            "email": "htmx@example.com",
            "message": "HTMX test message",
            "captcha": "red",
        }

        response = self.client.post(self.url, data=form_data, HTTP_HX_REQUEST="true")

        # Should render success template for HTMX when Telegram succeeds
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/success.html")

        # Verify Telegram service was called
        mock_send_telegram.assert_called_once_with(
            name="HTMX User", email="htmx@example.com", message="HTMX test message"
        )
