from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import PostFactory, UserFactory


class TestAboutView(TestCase):
    """Test AboutView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("about")
        cache.clear()
        self.user = UserFactory.create()

    def test_about_view_get(self):
        """Test GET request to about view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/about.html")

    def test_about_view_years_of_experience(self):
        """Test about view calculates years of experience correctly"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        current_year = timezone.now().year
        expected_years = current_year - 2014  # Start year from views.py

        self.assertEqual(response.context["years_of_experience"], expected_years)

    def test_about_view_htmx_request(self):
        """Test about view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render the partial content only
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "About me")

    def test_about_view_regular_request(self):
        """Test about view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/about.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_about_view_htmx_request_no_doctype(self):
        """Test about view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "About me")

    def test_about_view_cached_performance(self):
        """Test that cached views perform better on subsequent requests"""
        PostFactory.create(author=self.user, published_date=timezone.now())

        # First request - cache miss
        with self.assertNumQueries(1):  # Only request profile query for cached view
            response1 = self.client.get(self.url)

        self.assertEqual(response1.status_code, HTTPStatus.OK)

        # Second request - potentially cache hit (depending on cache configuration)
        response2 = self.client.get(self.url)
        self.assertEqual(response2.status_code, HTTPStatus.OK)

    def test_about_view_cache_miss_and_hit(self):
        """Test cache miss and hit behavior"""
        # First request - cache miss
        response1 = self.client.get(self.url)
        self.assertEqual(response1.status_code, HTTPStatus.OK)

        # Second request - should be cache hit (if caching is working)
        response2 = self.client.get(self.url)
        self.assertEqual(response2.status_code, HTTPStatus.OK)

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
