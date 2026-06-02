from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import PostFactory, UserFactory


class TestLayoutConsistency(TestCase):
    """Pages swapped into #content should carry their own layout wrapper."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory.create()
        cls.post = PostFactory.create(author=cls.user, published_date=timezone.now())

    def setUp(self) -> None:
        activate("en")

    def assert_same_content_layout(self, url: str) -> None:
        regular_response = self.client.get(url)
        htmx_response = self.client.get(url, headers={"HX-Request": "true"})

        self.assertEqual(regular_response.status_code, HTTPStatus.OK)
        self.assertEqual(htmx_response.status_code, HTTPStatus.OK)
        self.assertContains(regular_response, "<!DOCTYPE html>", count=1)
        self.assertNotContains(htmx_response, "<!DOCTYPE html>")
        self.assertContains(regular_response, 'id="content"', count=1)
        self.assertNotContains(htmx_response, 'id="content"')
        self.assertContains(regular_response, "page-layout", count=1)
        self.assertContains(htmx_response, "page-layout", count=1)

    def assert_history_restore_gets_full_page(self, url: str) -> None:
        response = self.client.get(
            url,
            headers={"HX-Request": "true", "HX-History-Restore-Request": "true"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<!DOCTYPE html>", count=1)
        self.assertContains(response, 'id="main-navbar"', count=1)
        self.assertContains(response, 'id="content"', count=1)

    def primary_page_urls(self) -> list[str]:
        return [
            reverse("about"),
            reverse("classes"),
            reverse("consultancy"),
            reverse("contact"),
            reverse("mentoring"),
            reverse("post_list"),
            reverse("post_detail", kwargs={"slug": self.post.slug}),
            reverse("search"),
            reverse("success"),
            reverse("error"),
            reverse("work"),
        ]

    def test_primary_pages_keep_same_layout_for_htmx_and_regular_requests(self) -> None:
        for url in self.primary_page_urls():
            with self.subTest(url=url):
                self.assert_same_content_layout(url)

    def test_primary_pages_render_full_document_for_htmx_history_restore_requests(self) -> None:
        for url in self.primary_page_urls():
            with self.subTest(url=url):
                self.assert_history_restore_gets_full_page(url)
