import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.factories import PostFactory
from blog.models import Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="function")
def published_post():
    return PostFactory.create()


@pytest.fixture(scope="function")
def unpublished_post():
    return PostFactory.create(published_date=None)


@pytest.mark.django_db
def test_update_post_method_not_allowed_no_auth(api_client, published_post):
    url = reverse("post-detail", args=[published_post.pk])
    post_data = {"title": "Updated title"}
    response = api_client.put(url, data=post_data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_post_method_not_allowed(api_client, published_post):
    url = reverse("post-detail", args=[published_post.id])
    post_data = {"title": "Updated title"}
    api_client.force_authenticate(user=published_post.author)
    response = api_client.put(url, data=post_data, format="json")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_list_published_posts(api_client, published_post):
    url = reverse("post-list")
    api_client.force_authenticate(user=published_post.author)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == Post.objects.published().count()


@pytest.mark.django_db
def test_list_all_posts(api_client, published_post, unpublished_post):
    url = reverse("post-list")
    api_client.force_authenticate(user=published_post.author)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == Post.objects.published().count()


@pytest.mark.django_db
def test_retrieve_published_post(api_client, published_post):
    url = reverse("post-detail", args=[published_post.id])
    api_client.force_authenticate(user=published_post.author)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == published_post.title


@pytest.mark.django_db
def test_retrieve_unpublished_post(api_client, unpublished_post):
    url = reverse("post-detail", args=[unpublished_post.id])
    api_client.force_authenticate(user=unpublished_post.author)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
