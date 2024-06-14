from http import HTTPStatus

import pytest
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from django.utils.translation import activate

from .factories import PostFactory, TagFactory, UserFactory


@pytest.fixture()
def posts(db):
    return PostFactory.create_batch(3)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "home",
        "post_list",
        "blog",
        "about",
        "search",
        "contact",
        "success",
        "error",
        "django.contrib.sitemaps.views.sitemaps",
    ],
)
def test_home_view(client, url, posts):
    url = reverse_lazy(url)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_post_by_slug(client, posts):
    for post in posts:
        response = client.get(reverse_lazy("post_detail", kwargs={"slug": post.slug}))
        assert response.status_code == 200


@pytest.mark.django_db
def test_get_post_list(client, posts):
    url = reverse_lazy("post_list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context_data["object_list"].count() == len(posts)


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["wp/admin", "admin"])
def test_get_bad_about(client, url):
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ("en", "es"))
def test_uses_index_template(client, lang):
    activate(lang)
    response = client.get(reverse_lazy("home"))
    assert response.request["PATH_INFO"] == f"/{lang}/"


class RelatedPostsViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.tag1 = TagFactory.create(word="test_tag1", slug="test-tag1")
        self.tag2 = TagFactory.create(word="test_tag2", slug="test-tag2")

        self.post1 = PostFactory.create(author=self.user, tags=[self.tag1])
        self.post2 = PostFactory.create(author=self.user, tags=[self.tag1, self.tag2])
        self.post3 = PostFactory.create(author=self.user, tags=[self.tag2])

        self.client = Client()
        self.client.force_login(self.user)
        self.url1 = reverse("related_posts", kwargs={"post_id": self.post1.pk})
        self.url2 = reverse("related_posts", kwargs={"post_id": self.post2.pk})
        self.url3 = reverse("related_posts", kwargs={"post_id": self.post3.pk})

    def test_related_posts_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url1)
        assert response.status_code == HTTPStatus.OK

    def test_related_posts_view_uses_correct_template(self):
        response = self.client.get(self.url2)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "blog/partials/posts/related_posts.html")
        self.assertTemplateUsed(response, "blog/utils/partial.html")
        self.assertTemplateUsed(response, "blog/posts/_related_posts.html")

    def test_related_posts(self):
        # post1 and post2 share the tag 'test_tag1', so they should be related.
        response = self.client.get(self.url1)
        self.assertContains(response, self.post2.title)
        self.assertNotContains(response, self.post1.title)  # A post shouldn't be related to itself
        self.assertNotContains(response, self.post3.title)  # post3 doesn't share a tag with post1

    def test_no_related_posts(self):
        # Get related posts for post3, which only shares a tag with post2.
        response = self.client.get(self.url3)
        assert response.status_code == HTTPStatus.OK
        self.assertNotContains(response, self.post1.title)
        self.assertNotContains(response, self.post3.title)  # A post shouldn't be related to itself
