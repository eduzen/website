import pytest
from django.urls import reverse_lazy

from blog.factories import PostFactory


@pytest.fixture()
def posts():
    return PostFactory.create_batch(3)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "home",
        "post_list",
        "post_archive",
        "blog",
        "about",
        "clases",
        "stuff",
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
def test_get_post(client, posts):
    for post in posts:
        response = client.get(reverse_lazy("post_detail", kwargs={"pk": post.id}))
        assert response.status_code == 200


@pytest.mark.django_db
def test_get_post_list(client, posts):
    url = reverse_lazy("post_list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context_data["object_list"].count() == len(posts)


@pytest.mark.django_db
def test_get_about(client, posts):
    response = client.get(reverse_lazy("about"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_bad_about(client, posts):
    response = client.get("wp/admin")
    assert response.status_code == 404
