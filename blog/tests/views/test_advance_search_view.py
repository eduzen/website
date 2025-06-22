from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from blog.forms import AdvanceSearchForm


class TestAdvanceSearchView(TestCase):
    """Test AdvanceSearch view functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("search")

    def test_get_search_page(self):
        """Test GET request returns search form"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/search.html")
        self.assertIsInstance(response.context["form"], AdvanceSearchForm)

    def test_post_valid_form_redirects(self):
        """Test POST with valid form data redirects to success"""
        form_data = {
            "q": "test query",
        }

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/success/")

    def test_post_invalid_form_shows_errors(self):
        """Test POST with invalid form data shows errors"""
        form_data = {}

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/search.html")
        self.assertContains(response, "This field is required")

    def test_search_with_empty_query(self):
        """Test search with empty query"""
        form_data = {"q": ""}

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "This field is required")

    def test_search_with_special_characters(self):
        """Test search with special characters"""
        form_data = {"q": '<script>alert("xss")</script>'}

        response = self.client.post(self.url, data=form_data)

        # Should redirect to success (assuming form validation passes)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_search_with_very_long_query(self):
        """Test search with very long query"""
        long_query = "search term " * 100
        form_data = {"q": long_query}

        response = self.client.post(self.url, data=form_data)

        # Behavior depends on form field max_length
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])

    def test_search_form_integration(self):
        """Test search form integration with view"""
        # Valid search
        response = self.client.post(self.url, data={"q": "python"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Invalid search (empty)
        response = self.client.post(self.url, data={"q": ""})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "This field is required")

    def test_search_form_htmx_submission(self):
        """Test search form submission via HTMX"""
        form_data = {"q": "python django"}

        response = self.client.post(self.url, data=form_data, HTTP_HX_REQUEST="true")

        # Should redirect to success page
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_search_and_filter_flow(self):
        """Test search and filtering flow"""
        # User visits search page
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # User performs search
        response = self.client.post(self.url, data={"q": "python"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
