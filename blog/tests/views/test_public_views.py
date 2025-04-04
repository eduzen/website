from http import HTTPStatus
from unittest.mock import patch

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
        cls.draft_post = PostFactory.create(author=cls.user, published_date=None)

    def setUp(self):
        activate("en")
        self.post_detail_url = reverse("blog_slug", kwargs={"slug": self.posts[0].slug})
        self.post_list_url = reverse("post_list")
        self.contact_url = reverse("contact")
        self.home_url = reverse("home")
        self.search_url = reverse("search")
        self.success_url = reverse("success")
        self.error_url = reverse("error")
        self.about_url = reverse("about")
        self.blog_url = reverse("blog")
        self.sitemap_url = reverse("django.contrib.sitemaps.views.sitemaps")

    def test_home_view(self):
        response = self.client.get(self.home_url)
        assert response.status_code == HTTPStatus.OK

    def test_blog_view(self):
        response = self.client.get(self.blog_url)
        assert response.status_code == HTTPStatus.OK

    def test_about_view(self):
        response = self.client.get(self.about_url)
        assert response.status_code == HTTPStatus.OK

    def test_search_view(self):
        response = self.client.get(self.search_url)
        assert response.status_code == HTTPStatus.OK

    def test_success_view(self):
        response = self.client.get(self.success_url)
        assert response.status_code == HTTPStatus.OK

    def test_error_view(self):
        response = self.client.get(self.error_url)
        assert response.status_code == HTTPStatus.OK

    def test_404_view(self):
        response = self.client.get("/404/")
        assert response.status_code == 404

    def test_sitemap_view(self):
        response = self.client.get(self.sitemap_url)
        assert response.status_code == HTTPStatus.OK

    def test_contact_view(self):
        response = self.client.get(self.contact_url)
        assert response.status_code == HTTPStatus.OK

    @patch("blog.forms.verify_captcha", return_value=True)
    @patch("blog.views.send_contact_message")
    def test_post_contact_form_valid(self, mock_send_message, mock_verify):
        mock_send_message.return_value = "Message sent"
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello there!",
            "captcha": "red",
        }
        response = self.client.post(self.contact_url, data=form_data)
        self.assertTemplateUsed(response, "blog/success.html")
        mock_verify.assert_called_once_with("red")
        mock_send_message.assert_called_once()
