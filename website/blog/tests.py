from django.test import TestCase
from django.contrib.auth.models import User

from .models import Post


class ModelTestCase(TestCase):
    """This class defines the test suite for the postlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.post_title = "Write world class code"
        self.user = User.objects.create(username='user1')
        self.post = Post(title=self.post_title, author=self.user)

    def tearDown(self):
        self.user.delete()
        self.post.delete()

    def test_model_can_create_a_bucketlist(self):
        """Test the postlist model can create a Post."""
        old_count = Post.objects.count()
        self.post.save()
        new_count = Post.objects.count()
        self.assertNotEqual(old_count, new_count)
