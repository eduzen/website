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

    def test_get_post_by_slug(self):
        response = self.client.get(self.post_detail_url)
        assert response.status_code == HTTPStatus.OK
