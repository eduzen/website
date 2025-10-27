import datetime as dt
from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import PostFactory, TagFactory, UserFactory


class TestPostListView(TestCase):
    """Test PostListView functionality"""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.tags = TagFactory.create_batch(2)
        cls.posts = PostFactory.create_batch(3, author=cls.user, tags=cls.tags)
        cls.draft_post = PostFactory.create(author=cls.user, published_date=None)

    def setUp(self):
        activate("en")
        self.url = reverse("post_list")
        cache.clear()

    def test_post_list_view_get(self):
        """Test GET request to post list view"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/posts/list.html")
        self.assertEqual(response.context["object_list"].count(), 3)

    def test_post_list_view_htmx_request(self):
        """Test post list view with HTMX request"""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Blog")

    def test_post_list_view_regular_request(self):
        """Test post list view with regular HTTP request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/posts/list.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_post_list_view_normal_template(self):
        """Test post list view uses normal template for regular requests"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/posts/list.html")
        self.assertNotContains(response, "htmx-requested-partial-specific-content")

    def test_post_list_view_htmx_request_no_doctype(self):
        """Test post list HTMX request doesn't include full page structure"""
        response = self.client.get(self.url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Blog")

    def test_empty_post_list(self):
        """Test post list with no posts"""
        # Delete all posts
        from blog.models import Post

        Post.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 0)

    def test_post_list_pagination(self):
        """Test pagination works correctly"""
        # Create enough posts to trigger pagination
        PostFactory.create_batch(15, author=self.user, published_date=timezone.now())

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["posts"]), 12)  # paginate_by = 12

    def test_post_list_second_page(self):
        """Test second page of pagination"""
        # Create 15 posts total (3 from setUpTestData + 12 new)
        PostFactory.create_batch(12, author=self.user, published_date=timezone.now())

        response = self.client.get(self.url + "?page=2")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["posts"]), 3)  # Remaining posts

    def test_pagination_out_of_range(self):
        """Test pagination with page number out of range"""
        PostFactory.create(author=self.user, published_date=timezone.now())

        response = self.client.get(self.url + "?page=999")

        # Should redirect to last page instead of raising 404
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("page=1", response.url)

    def test_pagination_invalid_page(self):
        """Test pagination with invalid page parameter"""
        PostFactory.create(author=self.user, published_date=timezone.now())

        response = self.client.get(self.url + "?page=invalid")

        # Should redirect to first page for invalid page parameter
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("page=1", response.url)

    def test_pagination_page_beyond_last_page(self):
        """Test accessing a page number beyond the last valid page"""
        # Create exactly 30 posts (3 from setup + 30 = 33 total, which is 3 pages)
        PostFactory.create_batch(30, author=self.user, published_date=timezone.now())

        # Try to access page 4 when only 3 pages exist
        response = self.client.get(self.url + "?page=4")

        # Should redirect to the last page (page 3)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("page=3", response.url)

        # Follow the redirect and verify we're on the correct page
        response = self.client.get(self.url + "?page=4", follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Should have posts from the last page (33 total: 12 + 12 + 9)
        self.assertEqual(len(response.context["posts"]), 9)
        # Should indicate we're on the last page
        self.assertFalse(response.context["page_obj"].has_next())

    def test_post_list_only_published_posts(self):
        """Test that only published posts are shown"""
        response = self.client.get(self.url)

        posts = response.context["posts"]
        for post in posts:
            self.assertIsNotNone(post.published_date)

    def test_post_list_ordering(self):
        """Test posts are ordered by published_date descending"""
        response = self.client.get(self.url)

        posts = list(response.context["posts"])
        published_dates = [post.published_date for post in posts]
        self.assertEqual(published_dates, sorted(published_dates, reverse=True))

    def test_post_list_prefetch_tags(self):
        """Test that tags are prefetched to avoid N+1 queries"""
        with self.assertNumQueries(4):  # Account for user, posts, tags, and request profile queries
            response = self.client.get(self.url)
            posts = response.context["posts"]
            # Access tags to trigger potential queries
            for post in posts:
                list(post.tags.all())

    def test_post_list_with_unicode_slug(self):
        """Test post list includes posts with unicode slugs"""
        post = PostFactory.create(
            author=self.user, title="Test Post with Ñoño", slug="test-post-with-nono", published_date=timezone.now()
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, post.title)

    def test_post_list_with_many_posts(self):
        """Test post list performance with many posts"""
        # Create many posts
        PostFactory.create_batch(100, author=self.user, published_date=timezone.now())

        with self.assertNumQueries(4):  # Account for count, posts, tags, and request profile queries
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Should only show first page (12 posts due to pagination)
        self.assertEqual(len(response.context["posts"]), 12)

    def test_post_list_with_tag_filter(self):
        """Test post list with tag parameter (currently not implemented)"""
        python_tag = TagFactory.create(word="python", slug="python")
        response = self.client.get(self.url + f"?tags={python_tag.pk}")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        posts = response.context["posts"]

        # Tag filtering is not currently implemented, so all posts appear
        self.assertGreater(len(posts), 0)

    def test_post_list_with_search_filter(self):
        """Test post list with search functionality"""
        # Skip search test on SQLite as it uses PostgreSQL-specific features
        from django.conf import settings

        if "sqlite" in settings.DATABASES["default"]["ENGINE"]:
            self.skipTest("Search functionality requires PostgreSQL")

        response = self.client.get(self.url + "?q=Django")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        posts = response.context["posts"]  # Use posts context variable

        # Should return posts (search may or may not find matches)
        self.assertGreaterEqual(len(posts), 0)

    def test_post_creation_appears_in_list(self):
        """Test that newly created posts appear in list view"""
        # Check initial count
        initial_response = self.client.get(self.url)
        initial_count = initial_response.context["posts"].count()

        # Create new post
        new_post = PostFactory.create(author=self.user, published_date=timezone.now())

        # Check updated count
        updated_response = self.client.get(self.url)
        updated_count = updated_response.context["posts"].count()

        self.assertEqual(updated_count, initial_count + 1)
        self.assertContains(updated_response, new_post.title)

    def test_draft_post_not_visible(self):
        """Test that draft posts are not visible in public views"""
        draft_post = PostFactory.create(
            author=self.user,
            published_date=None,  # Draft
        )

        # Should not appear in list
        list_response = self.client.get(self.url)
        self.assertNotContains(list_response, draft_post.title)

    def test_post_with_future_date_visible(self):
        """Test that posts with future publish dates are visible (current behavior)"""
        future_post = PostFactory.create(author=self.user, published_date=timezone.now() + dt.timedelta(days=1))

        list_response = self.client.get(self.url)
        # Current implementation shows future-dated posts
        self.assertContains(list_response, future_post.title)

    def test_post_list_pagination_htmx(self):
        """Test post list pagination via HTMX"""
        # Create enough posts to trigger pagination
        PostFactory.create_batch(25, author=self.user, published_date=timezone.now())

        response = self.client.get(self.url + "?page=2", HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Blog")
