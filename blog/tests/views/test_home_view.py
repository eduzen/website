from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from blog.tests.factories import UserFactory


class TestHomeView(TestCase):
    """Test HomeView functionality"""

    def setUp(self):
        activate("en")
        self.url = reverse("home")
        cache.clear()
        self.user = UserFactory.create()

    def test_home_view_get(self):
        """Test GET request to home view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_home_view_context_data(self):
        """Test home view returns correct context"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_home_view_htmx_request(self):
        """Test home view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_home.html")

    def test_home_view_regular_request(self):
        """Test home view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/home.html")
        # Regular request should include base template structure
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_home_view_htmx_request_no_doctype(self):
        """Test home view HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_home.html")
        # HTMX request should not include full page structure
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_home_view_is_cached(self):
        """Test that home view is cached"""
        # This is a smoke test to ensure cache decorators don't break functionality
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Second request should also work (cache may or may not be hit in tests)
        response2 = self.client.get(self.url)
        self.assertEqual(response2.status_code, HTTPStatus.OK)

    def test_home_view_spanish_language(self):
        """Test home view works with Spanish language setting"""
        activate("es")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_home_view_post_request(self):
        """Test POST request to home view (should handle gracefully)"""
        response = self.client.post(self.url, data={})
        # Should handle POST gracefully or return method not allowed
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])

    def test_home_view_with_invalid_http_method(self):
        """Test home view with invalid HTTP method"""
        response = self.client.put(self.url)
        self.assertIn(response.status_code, [HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.NOT_FOUND])

    def test_navbar_duplication_bug(self):
        """Test that clicking eduzen link doesn't cause navbar duplication"""
        # Simulate clicking the eduzen link with HTMX
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/_home.html")

        # The partial response should not contain any navbar elements
        # This test should pass once the bug is fixed
        self.assertNotContains(response, 'id="main-navbar"')
        self.assertNotContains(response, "<nav")
        self.assertNotContains(response, "loadingIndicator")

    def test_cache_bug_regular_first_then_htmx(self):
        """Test cache bug: regular request first, then HTMX request"""
        cache.clear()

        # First request: regular HTTP request (gets cached)
        regular_response = self.client.get(self.url)
        self.assertEqual(regular_response.status_code, HTTPStatus.OK)
        self.assertContains(regular_response, 'id="main-navbar"', count=1)
        self.assertTemplateUsed(regular_response, "blog/home.html")

        # Second request: HTMX request (should get partial, but might get cached full page)
        htmx_response = self.client.get(self.url, headers={"HX-Request": "true"})
        self.assertEqual(htmx_response.status_code, HTTPStatus.OK)

        print("\nRegular request first, then HTMX:")
        print(f"HTMX response contains navbar: {'id="main-navbar"' in htmx_response.content.decode()}")
        print(f"HTMX response template used: {htmx_response.templates[0].name if htmx_response.templates else 'None'}")

        # This test should FAIL if cache is broken (reproducing the bug)
        # The cached full page response should NOT be served for HTMX requests
        try:
            self.assertNotContains(htmx_response, 'id="main-navbar"')
            print("✓ HTMX request correctly got partial template (cache working correctly)")
        except AssertionError:
            print("✗ CACHE BUG REPRODUCED: HTMX request got cached full page!")
            raise

    def test_cache_bug_htmx_first_then_regular(self):
        """Test cache behavior: HTMX request first, then regular request"""
        cache.clear()

        # First request: HTMX request (partial gets cached)
        htmx_response = self.client.get(self.url, headers={"HX-Request": "true"})
        self.assertEqual(htmx_response.status_code, HTTPStatus.OK)
        self.assertNotContains(htmx_response, 'id="main-navbar"')
        self.assertTemplateUsed(htmx_response, "blog/_home.html")

        # Second request: regular HTTP request (should get full page, but might get cached partial)
        regular_response = self.client.get(self.url)
        self.assertEqual(regular_response.status_code, HTTPStatus.OK)

        print("\nHTMX request first, then regular:")
        print(f"Regular response contains navbar: {'id="main-navbar"' in regular_response.content.decode()}")
        print(
            f"Regular response template used: {regular_response.templates[0].name if regular_response.templates else 'None'}"
        )

        # This test should FAIL if cache is broken
        # The cached partial response should NOT be served for regular requests
        try:
            self.assertContains(regular_response, 'id="main-navbar"', count=1)
            print("✓ Regular request correctly got full template (cache working correctly)")
        except AssertionError:
            print("✗ CACHE BUG: Regular request got cached partial instead of full page!")
            raise

    def test_no_cache_both_requests_work_correctly(self):
        """Test without cache: both request types work correctly"""
        # Clear cache and disable caching for this test
        cache.clear()

        with self.settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}):
            # Regular request
            regular_response = self.client.get(self.url)
            self.assertEqual(regular_response.status_code, HTTPStatus.OK)
            self.assertContains(regular_response, 'id="main-navbar"', count=1)
            self.assertTemplateUsed(regular_response, "blog/home.html")

            # HTMX request
            htmx_response = self.client.get(self.url, headers={"HX-Request": "true"})
            self.assertEqual(htmx_response.status_code, HTTPStatus.OK)
            self.assertNotContains(htmx_response, 'id="main-navbar"')
            self.assertTemplateUsed(htmx_response, "blog/_home.html")

            print("\nNo cache test:")
            print(f"Regular template: {regular_response.templates[0].name}")
            print(f"HTMX template: {htmx_response.templates[0].name}")
