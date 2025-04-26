from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import PostFactory, TagFactory, UserFactory


class TestRelatedPostsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create all of your test data only once
        cls.user = UserFactory.create()
        cls.tag1 = TagFactory.create(word="test_tag1", slug="test-tag1")
        cls.tag2 = TagFactory.create(word="test_tag2", slug="test-tag2")

        cls.post1 = PostFactory.create(author=cls.user, tags=[cls.tag1], published_date=timezone.now())
        cls.post2 = PostFactory.create(author=cls.user, tags=[cls.tag1, cls.tag2], published_date=timezone.now())
        cls.post3 = PostFactory.create(author=cls.user, tags=[cls.tag2], published_date=timezone.now())

    def setUp(self):
        # setUp still runs before *every* test method—lightweight things only
        activate("en")
        self.url1 = reverse("related_posts", kwargs={"post_id": self.post1.pk})
        self.url2 = reverse("related_posts", kwargs={"post_id": self.post2.pk})
        self.url3 = reverse("related_posts", kwargs={"post_id": self.post3.pk})

    def test_related_posts_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url1)
        assert response.status_code == HTTPStatus.OK

    def test_related_posts_view_uses_correct_template(self):
        response = self.client.get(self.url2)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "blog/posts/related_posts.html")
        self.assertTemplateUsed(response, "core/utils/base.html")
        self.assertTemplateUsed(response, "blog/posts/_related_posts.html")

    def test_related_posts_view_uses_correct_template_for_htmx(self):
        response = self.client.get(self.url2, headers={"HX-Request": "true"})
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "blog/partials/posts/related_posts.html")
        self.assertTemplateUsed(response, "core/utils/partial.html")
        self.assertTemplateUsed(response, "blog/posts/_related_posts.html")

    def test_related_posts(self):
        # post1 and post2 share the tag 'test_tag1'
        response = self.client.get(self.url1)
        self.assertContains(response, self.post2.title)
        self.assertNotContains(response, self.post1.title)
        self.assertNotContains(response, self.post3.title)

    def test_no_related_posts(self):
        # post3 only shares a tag with post2, so post1 is not related
        response = self.client.get(self.url3)
        assert response.status_code == HTTPStatus.OK
        self.assertNotContains(response, self.post1.title)
        self.assertNotContains(response, self.post3.title)
