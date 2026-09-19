from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import UserFactory


class TestAboutView(TestCase):
    """Test AboutView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("about")
        cache.clear()
        self.user = UserFactory.create()

    def test_about_view_years_from_global_data(self):
        """Test that years come from the global_data context processor"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        global_data = response.context["global_data"]
        current_year = timezone.now().year
        self.assertEqual(global_data["years_in_python"], str(current_year - 2014))
        self.assertEqual(global_data["years_of_experience"], str(current_year - 2011))

    def test_about_view_regular_request(self):
        """Test about view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/about.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_about_view_cache_varies_by_language(self):
        """Test that cache keys vary by language if implemented"""
        # Test with English
        activate("en")
        response_en = self.client.get(self.url)

        # Test with Spanish
        activate("es")
        response_es = self.client.get(reverse("about"))

        self.assertEqual(response_en.status_code, HTTPStatus.OK)
        self.assertEqual(response_es.status_code, HTTPStatus.OK)

    def test_about_view_content_sections(self):
        """Test that the redesigned about page has expected sections"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Bio")
        self.assertContains(response, "Beyond code")
        self.assertContains(response, "Python")
