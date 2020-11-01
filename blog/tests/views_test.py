import pytest
from django.urls import reverse_lazy
from django.utils.translation import activate

from .factories import PostFactory


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
        "sucess",
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
