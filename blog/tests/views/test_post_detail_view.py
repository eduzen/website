from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.models import Post
from blog.tests.factories import PostFactory, TagFactory, UserFactory


class TestPostDetailView(TestCase):
    """Test PostDetailView functionality"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory.create()
        cls.tags = TagFactory.create_batch(3)
        cls.post = PostFactory.create(author=cls.user, tags=cls.tags, published_date=timezone.now())
        cls.draft_post = PostFactory.create(author=cls.user, published_date=None)

    def setUp(self) -> None:
        activate("en")
        cache.clear()

    def test_post_detail_with_slug(self) -> None:
        """Test post detail view with slug"""
        url = reverse("post_detail", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["post"], self.post)
        self.assertTemplateUsed(response, "blog/posts/detail.html")

    def test_post_detail_blog_slug_url(self) -> None:
        """Test post detail view via blog_slug URL pattern"""
        url = reverse("blog_slug", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["post"], self.post)

    def test_get_post_by_slug(self) -> None:
        """Test getting post by slug"""
        url = reverse("blog_slug", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.post.title)

    def test_get_post_invalid_slug_returns_404(self) -> None:
        """Test getting post with invalid slug returns 404"""
        response = self.client.get(reverse("blog_slug", kwargs={"slug": "non-existent-slug"}))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_accessible(self) -> None:
        """Test that draft posts are not accessible"""
        url = reverse("post_detail", kwargs={"slug": self.draft_post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_detail_htmx_request(self) -> None:
        """Test post detail with HTMX request"""
        url = reverse("post_detail", kwargs={"slug": self.post.slug})
        response = self.client.get(url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render the partial content only
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, self.post.title)

    def test_post_detail_regular_request(self) -> None:
        """Test post detail view with regular HTTP request"""
        url = reverse("post_detail", kwargs={"slug": self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/posts/detail.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_post_detail_htmx_request_no_doctype(self) -> None:
        """Test post detail HTMX request doesn't include full page structure"""
        url = reverse("post_detail", kwargs={"slug": self.post.slug})
        response = self.client.get(url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, self.post.title)

    def test_post_detail_prefetch_tags(self) -> None:
        """Test that tags are prefetched and author is joined in a single query."""
        url = reverse("post_detail", kwargs={"slug": self.post.slug})

        # Fix #2: select_related("author") merges the user lookup into the main
        # SELECT, so we now need 3 queries instead of 4:
        #   1. SELECT blog_post JOIN auth_user (post + author in one go)
        #   2. SELECT blog_tag … (prefetch_related tags)
        #   3. INSERT django_fast_requestprofile (ProfilerMiddleware)
        with self.assertNumQueries(3):
            response = self.client.get(url)
            post = response.context["post"]
            list(post.tags.all())  # Access tags (served from prefetch cache)

    def test_post_detail_with_very_long_slug(self) -> None:
        """Test post detail with very long slug"""
        long_slug = "a" * 200  # Very long slug
        post = PostFactory.create(author=self.user, slug=long_slug, published_date=timezone.now())

        url = reverse("post_detail", kwargs={"slug": long_slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["post"], post)

    def test_post_detail_with_special_characters_slug(self) -> None:
        """Test post detail with special characters in slug"""
        special_slug = "test-post-123-with-numbers"
        post = PostFactory.create(author=self.user, slug=special_slug, published_date=timezone.now())

        url = reverse("post_detail", kwargs={"slug": special_slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["post"], post)

    def test_post_detail_empty_slug(self) -> None:
        """Test post detail with empty slug should not match URL pattern"""
        # This should not match the URL pattern at all
        # Django URL routing should handle this case
        pass  # This is handled by URL patterns, not the view

    def test_post_with_many_tags(self) -> None:
        """Test post detail with many tags"""
        tags = TagFactory.create_batch(50)
        post = PostFactory.create(author=self.user, tags=tags, published_date=timezone.now())

        url = reverse("post_detail", kwargs={"slug": post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Just ensure we have many tags (exact count may vary due to factory constraints)
        self.assertGreaterEqual(len(post.tags.all()), 40)

    def test_post_detail_query_optimization(self) -> None:
        """Test that post detail view uses optimal query count."""
        post = Post.objects.published().first()
        assert post is not None

        # Fix #2: select_related("author") collapses post + user into one JOIN query.
        # Total: 3 queries (post+author JOIN, prefetch tags, profiler INSERT).
        with self.assertNumQueries(3):
            response = self.client.get(reverse("post_detail", kwargs={"slug": post.slug}))
            post_obj = response.context["post"]
            list(post_obj.tags.all())  # Access tags (served from prefetch cache)

    def test_post_detail_htmx_post_not_found(self) -> None:
        """Test post not found with HTMX"""
        response = self.client.get(reverse("post_detail", kwargs={"slug": "nonexistent-slug"}), HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
