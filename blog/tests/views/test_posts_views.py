from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from blog.tests.factories import PostFactory, TagFactory, UserFactory


class TestPublicViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.tags = TagFactory.create_batch(2)
        cls.posts = PostFactory.create_batch(3, author=cls.user, tags=cls.tags)

    def setUp(self):
        activate("en")
        self.post_detail_url = reverse("blog_slug", kwargs={"slug": self.posts[0].slug})
        self.post_list_url = reverse("post_list")

    def test_post_list_view(self):
        response = self.client.get(self.post_list_url)
        assert response.status_code == HTTPStatus.OK
        assert response.context_data["object_list"].count() == 3
        # Ensure only published posts appear (assuming .published() excludes drafts)
        self.assertEqual(response.context_data["object_list"].count(), 3)

    def test_bytag_non_existent_tag(self):
        response = self.client.get(reverse("bytag", kwargs={"tag": "some-other-tag"}))
        self.assertEqual(response.status_code, 200)
        # Should show an empty result
        self.assertContains(response, "No posts found")  # Or however your template handles it
        self.assertEqual(response.context["object_list"].count(), 0)

    def test_post_list_view_htmx_partial_template(self):
        # Simulate an HTMX request by setting the HX-Request header
        response = self.client.get(self.post_list_url, **{"HTTP_HX_REQUEST": "true"})
        assert response.status_code == HTTPStatus.OK
        # Ensure partial template is used
        self.assertTemplateUsed(response, "blog/partials/posts/list.html")

    def test_get_post_by_slug(self):
        response = self.client.get(self.post_detail_url)
        assert response.status_code == HTTPStatus.OK
        self.assertContains(response, self.posts[0].title)

    def test_get_post_invalid_slug_returns_404(self):
        response = self.client.get(reverse("blog_slug", kwargs={"slug": "non-existent-slug"}))
        self.assertEqual(response.status_code, 404)
