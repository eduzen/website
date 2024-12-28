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

    def test_home_view(self):
        home_url = reverse("home")
        response = self.client.get(home_url)
        assert response.status_code == HTTPStatus.OK

    def test_blog_view(self):
        response = self.client.get(reverse("blog"))
        assert response.status_code == HTTPStatus.OK

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        assert response.status_code == HTTPStatus.OK

    def test_contact_view(self):
        response = self.client.get(reverse("contact"))
        assert response.status_code == HTTPStatus.OK

    def test_search_view(self):
        response = self.client.get(reverse("search"))
        assert response.status_code == HTTPStatus.OK

    def test_success_view(self):
        response = self.client.get(reverse("success"))
        assert response.status_code == HTTPStatus.OK

    def test_error_view(self):
        response = self.client.get(reverse("error"))
        assert response.status_code == HTTPStatus.OK

    def test_404_view(self):
        response = self.client.get("/404/")
        assert response.status_code == 404

    def test_sitemap_view(self):
        response = self.client.get(reverse("django.contrib.sitemaps.views.sitemaps"))
        assert response.status_code == HTTPStatus.OK
