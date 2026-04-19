from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class TestWorkView(TestCase):
    """Test WorkView functionality"""

    def setUp(self) -> None:
        activate("en")
        self.url = reverse("work")
        cache.clear()

    def test_work_view_get(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/work.html")

    def test_work_view_contains_projects(self) -> None:
        response = self.client.get(self.url)

        self.assertContains(response, "Maite Blog")
        self.assertContains(response, "Groomit")
        self.assertContains(response, "Champi.dev")
        self.assertContains(response, "Althaia")

    def test_work_view_htmx_request(self) -> None:
        response = self.client.get(self.url, headers={"hx-request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Work")

    def test_work_view_regular_request_has_doctype(self) -> None:
        response = self.client.get(self.url)

        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_work_view_project_links(self) -> None:
        response = self.client.get(self.url)

        self.assertContains(response, "maiteblog.com")
        self.assertContains(response, "groomit.io")
        self.assertContains(response, "champi.dev")
        self.assertContains(response, "althaia.nl")
