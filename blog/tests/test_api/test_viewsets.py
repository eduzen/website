from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def setUp(self):
        self.url_list = reverse("post-list")
        self.user = User.objects.create_user(username="test", password="test")

    def test_list_post_non_auth(self):
        response = self.client.get(self.url_list)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_post_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_list)

        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url_list, data={"title": "test", "content": "test"})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
