from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.post_data = {
            'author': 'Go to Ibiza',
            'title': 1,
            'pompadour': 1,
            'published_date': 1,
            'tags': 1,
            'text': 1,
        }

        self.response = self.client.post(
            reverse('post_create'),
            self.post_data,
            format="json"
        )


    def test_api_can_create_a_post(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_a_tag(self):
        response = self.client.post(
            reverse('tag_create'),
            {'word': 'test', 'slug': 'test'},
            format='json',
        )

        assert response == status.HTTP_201_CREATED
