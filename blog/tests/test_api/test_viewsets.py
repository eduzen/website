from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_list_post(self):
        url = reverse("post-list")

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
