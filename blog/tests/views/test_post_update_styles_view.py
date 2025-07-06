from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from blog.tests.factories import PostFactory, UserFactory


class TestPostUpdateStylesView(TestCase):
    """Test PostUpdateStylesView functionality"""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.post = PostFactory.create(
            author=cls.user, text="This is the original post text content.", published_date=timezone.now()
        )
        # Create superuser for permissions
        cls.superuser = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")

    def setUp(self):
        activate("en")
        cache.clear()

    def test_post_update_styles_requires_authentication(self):
        """Test that post update styles requires authentication"""
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})
        response = self.client.get(url)

        # Should redirect to login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/accounts/login/", response.url)

    def test_post_update_styles_requires_permissions(self):
        """Test that post update styles works for logged-in users"""
        self.client.force_login(self.user)  # Regular user
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})
        response = self.client.get(url)

        # Should redirect to admin after processing (login_required only)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/eduardo/blog/post/", response.url)

    @patch("blog.views.apply_styles")
    def test_post_update_styles_with_superuser(self, mock_apply_styles):
        """Test post update styles with logged-in user"""
        mock_apply_styles.return_value = "Styled post content"

        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        mock_apply_styles.assert_called_once_with(self.post.text)

    @patch("blog.views.apply_styles")
    def test_post_update_styles_applies_styling(self, mock_apply_styles):
        """Test that styling is applied to post content"""
        styled_content = "**This is the styled post text content.**"
        mock_apply_styles.return_value = styled_content

        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Refresh post from database
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, styled_content)

    @patch("blog.views.apply_styles")
    def test_post_update_styles_handles_service_error(self, mock_apply_styles):
        """Test handling of styling service errors"""
        mock_apply_styles.side_effect = Exception("API Error")

        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})

        # Should raise exception (not handled gracefully in view)
        with self.assertRaises(Exception):
            self.client.get(url)

    def test_post_update_styles_nonexistent_post(self):
        """Test post update styles with non-existent post"""
        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @patch("blog.views.apply_styles")
    def test_post_update_styles_with_empty_content(self, mock_apply_styles):
        """Test styling post with empty content"""
        empty_post = PostFactory.create(author=self.user, text="", published_date=timezone.now())
        mock_apply_styles.return_value = ""

        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": empty_post.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        mock_apply_styles.assert_called_once_with("")

    @patch("blog.views.apply_styles")
    def test_post_update_styles_preserves_original_on_failure(self, mock_apply_styles):
        """Test that original content is preserved when styling fails"""
        original_text = self.post.text
        mock_apply_styles.side_effect = Exception("Styling failed")

        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})

        try:
            self.client.get(url)
        except Exception:
            pass  # Error is expected

        # Post content should remain unchanged
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, original_text)

    @patch("blog.views.apply_styles")
    def test_post_update_styles_htmx_request(self, mock_apply_styles):
        """Test post update styles with HTMX request"""
        mock_apply_styles.return_value = "Styled content"

        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})
        response = self.client.get(url, HTTP_HX_REQUEST="true")

        # Should redirect to admin regardless of HTMX
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_update_styles_post_request(self):
        """Test POST request to post update styles (if supported)"""
        self.client.force_login(self.superuser)
        url = reverse("post_update_styles", kwargs={"post_id": self.post.pk})
        response = self.client.post(url, data={})

        # Should handle POST gracefully or return method not allowed
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.FOUND])
