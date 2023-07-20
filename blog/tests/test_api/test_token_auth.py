import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_get_token_GET():
    url = reverse("api-token-auth")
    client = APIClient()

    response = client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_get_token_bad_request():
    url = reverse("api-token-auth")
    client = APIClient()

    response = client.post(url, data={"username": "test", "password": "test"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_token():
    url = reverse("api-token-auth")
    user = User.objects.create_user(username="test", password="test")
    client = APIClient()

    response = client.post(url, data={"username": user.username, "password": "test"})
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
