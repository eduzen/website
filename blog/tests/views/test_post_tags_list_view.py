from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import PostFactory, TagFactory, UserFactory


class TestPostTagsListView(TestCase):
    """Test PostTagsListView functionality"""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.python_tag = TagFactory.create(word="python", slug="python")
        cls.django_tag = TagFactory.create(word="django", slug="django")

        cls.python_posts = PostFactory.create_batch(
            3, author=cls.user, tags=[cls.python_tag], published_date=timezone.now()
        )
        cls.django_posts = PostFactory.create_batch(
            2, author=cls.user, tags=[cls.django_tag], published_date=timezone.now()
        )

    def setUp(self):
        activate("en")
        cache.clear()

    def test_bytag_non_existent_tag(self):
        """Test bytag view with non-existent tag"""
        response = self.client.get(reverse("bytag", kwargs={"tag": "some-other-tag"}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["object_list"].count(), 0)
        self.assertContains(response, "We could not find what you are looking for...")

    def test_posts_filtered_by_tag(self):
        """Test posts are filtered by specific tag"""
        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 3)

        for post in response.context["posts"]:
            self.assertIn(self.python_tag, post.tags.all())

    def test_tag_name_in_context(self):
        """Test tag name is properly set in context"""
        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url)

        self.assertEqual(response.context["tag"], "Python")  # Title case

    def test_nonexistent_tag(self):
        """Test behavior with non-existent tag"""
        url = reverse("bytag", kwargs={"tag": "nonexistent"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 0)

    def test_tag_with_hyphens(self):
        """Test tag with hyphens is handled correctly"""
        tag = TagFactory.create(word="machine-learning", slug="machine-learning")
        PostFactory.create(author=self.user, tags=[tag], published_date=timezone.now())

        url = reverse("bytag", kwargs={"tag": "machine-learning"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["tag"], "Machine-Learning")
        self.assertEqual(response.context["posts"].count(), 1)

    def test_post_tags_list_view_regular_request(self):
        """Test post tags list view with regular HTTP request"""
        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "blog/posts/list.html")
        self.assertContains(response, "<!DOCTYPE html>", count=1)

    def test_post_tags_list_view_htmx_request(self):
        """Test post tags list view with HTMX request"""
        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url, headers={"HX-Request": "true"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # With django-template-partials, HTMX requests render only the partial content
        self.assertNotContains(response, "<!DOCTYPE html>")
        self.assertContains(response, "Blog")

    def test_tag_with_empty_posts(self):
        """Test tag view with tag that has no posts"""
        TagFactory.create(word="empty-tag", slug="empty-tag")

        url = reverse("bytag", kwargs={"tag": "empty-tag"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 0)
        self.assertEqual(response.context["tag"], "Empty-Tag")

    def test_tag_case_sensitivity(self):
        """Test tag filtering is case sensitive in URL but displays properly"""
        # Use existing python tag from setup
        PostFactory.create(author=self.user, tags=[self.python_tag], published_date=timezone.now())

        # Test lowercase URL
        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 4)  # 3 from setup + 1 new
        self.assertEqual(response.context["tag"], "Python")

    def test_tag_with_numbers_and_hyphens(self):
        """Test tag with numbers and hyphens"""
        tag = TagFactory.create(word="python-3-11", slug="python-3-11")
        PostFactory.create(author=self.user, tags=[tag], published_date=timezone.now())

        url = reverse("bytag", kwargs={"tag": "python-3-11"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 1)
        self.assertEqual(response.context["tag"], "Python-3-11")

    def test_tag_with_no_published_posts(self):
        """Test tag view when tag has no published posts"""
        tag = TagFactory.create(word="empty", slug="empty")
        # Create draft post with this tag
        PostFactory.create(
            author=self.user,
            tags=[tag],
            published_date=None,  # Draft
        )

        response = self.client.get(reverse("bytag", kwargs={"tag": "empty"}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["posts"].count(), 0)

    def test_tag_capitalization_with_different_locales(self):
        """Test tag capitalization works with different locales"""
        tag = TagFactory.create(word="español", slug="espanol")
        PostFactory.create(author=self.user, tags=[tag], published_date=timezone.now())

        activate("es")
        url = reverse("bytag", kwargs={"tag": "espanol"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["tag"], "Espanol")

    def test_tag_pagination(self):
        """Test pagination works correctly for tags"""
        # Create 15 posts with python tag to trigger pagination
        PostFactory.create_batch(15, author=self.user, tags=[self.python_tag], published_date=timezone.now())

        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["posts"]), 12)  # paginate_by = 12

    def test_tag_pagination_page_beyond_last_page(self):
        """Test accessing a page number beyond the last valid page for tag view"""
        # Create exactly 30 posts with python tag (3 from setup + 30 = 33 total)
        PostFactory.create_batch(30, author=self.user, tags=[self.python_tag], published_date=timezone.now())

        url = reverse("bytag", kwargs={"tag": "python"})
        # Try to access page 4 when only 3 pages exist
        response = self.client.get(url + "?page=4")

        # Should redirect to the last page (page 3)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("page=3", response.url)

        # Follow the redirect and verify we're on the correct page
        response = self.client.get(url + "?page=4", follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Should have posts from the last page (33 total: 12 + 12 + 9)
        self.assertEqual(len(response.context["posts"]), 9)
        # Should indicate we're on the last page
        self.assertFalse(response.context["page_obj"].has_next())

    def test_tag_pagination_invalid_page(self):
        """Test pagination with invalid page parameter for tag view"""
        PostFactory.create(author=self.user, tags=[self.python_tag], published_date=timezone.now())

        url = reverse("bytag", kwargs={"tag": "python"})
        response = self.client.get(url + "?page=invalid")

        # Should redirect to first page for invalid page parameter
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("page=1", response.url)
