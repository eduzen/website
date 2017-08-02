from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token


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
        self.user = User.objects.create_user(
            username='eduzen', email='test@test.com', password='top_secret')


        self.response = self.client.post(
            reverse('post_create'),
            self.post_data,
            format="json"
        )

    def tearDown(self):
        self.client.logout()
