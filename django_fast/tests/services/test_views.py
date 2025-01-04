from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CacheExplorerViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("cache_explorer")
        cls.staff_user = User.objects.create_user(username="staff", password="password", is_staff=True)
        cls.regular_user = User.objects.create_user(username="regular", password="password", is_staff=False)

    def test_access_for_staff(self):
        self.client.login(username="staff", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cache Explorer")

    def test_access_for_non_staff(self):
        self.client.login(username="regular", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, f"{reverse('admin:login')}?next={self.url}")

    def test_render_cache_settings(self):
        self.client.login(username="staff", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        cache_settings = response.context["cache_settings"]
        self.assertIn("default", cache_settings)  # Assuming a default cache is configured
        self.assertIn("status", response.context)

    def test_status_dict_contains_expected_status(self):
        self.client.login(username="staff", password="password")
        response = self.client.get(self.url)
        status_dict = response.context["status"]
        self.assertIn("default", status_dict)
        self.assertIn(status_dict["default"], ["🟢 Live", "🔴 Unavailable"])
