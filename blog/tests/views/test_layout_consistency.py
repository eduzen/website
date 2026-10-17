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

    def test_site_shell_uses_the_shared_outer_container(self) -> None:
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'class="site-container flex items-center justify-between py-3"')
        self.assertContains(response, '<div class="site-container">', count=1)

    def test_post_detail_uses_the_shared_reading_column(self) -> None:
        response = self.client.get(reverse("post_detail", kwargs={"slug": self.post.slug}))

        self.assertContains(response, '<article class="page-prose">')
        self.assertContains(response, 'id="related-post-container"')

    def page_header_urls(self) -> list[str]:
        return [
            reverse("about"),
            reverse("blog"),
            reverse("classes"),
            reverse("consultancy"),
            reverse("contact"),
            reverse("mentoring"),
            reverse("post_list"),
            reverse("search"),
            reverse("work"),
        ]

    def test_inner_pages_use_shared_page_header(self) -> None:
        for url in self.page_header_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertContains(response, "page-header")

    def test_home_keeps_left_aligned_hero_without_page_header(self) -> None:
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'class="hero"')
        self.assertNotContains(response, "page-header")

    def test_contact_uses_shared_header_and_details_structure(self) -> None:
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "page-layout")
        self.assertContains(response, "page-header")
        self.assertContains(response, "contact-details")

    def test_search_uses_reading_column_and_warm_form(self) -> None:
        response = self.client.get(reverse("search"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Advanced Search")
        self.assertContains(response, "page-prose")
        self.assertContains(response, "warm-form")

    def test_about_and_classes_use_shared_cta(self) -> None:
        for url in (reverse("about"), reverse("classes")):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertContains(response, "about-cta")
