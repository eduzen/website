import unittest
from unittest.mock import Mock, patch

from requests.exceptions import HTTPError

from blog.services.telegram import send_message

# Patch TELEGRAM_TOKEN to a "real" value so the guard doesn't skip sending
REAL_TOKEN_PATCH = patch("blog.services.telegram.TELEGRAM_TOKEN", "real-bot-token")


class SendMessageTest(unittest.TestCase):
    # Happy path
    @REAL_TOKEN_PATCH
    @patch("blog.services.telegram.requests.post")
    def test_send_message_success(self, mock_post: Mock) -> None:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None  # This means no error
        mock_response.json.return_value = {"ok": True, "result": "Some response data"}

        mock_post.return_value = mock_response

        response = send_message("Hello!")

        assert response == {"ok": True, "result": "Some response data"}
        mock_post.assert_called_once()

    # Unhappy path
    @REAL_TOKEN_PATCH
    @patch("blog.services.telegram.requests.post")
    def test_send_message_failure(self, mock_post: Mock) -> None:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("An error occurred")

        mock_post.return_value = mock_response

        with self.assertRaises(HTTPError):
            send_message("Hello!")
        mock_post.assert_called_once()

    def test_send_message_skips_when_not_configured(self) -> None:
        """When TELEGRAM_TOKEN is a placeholder, send_message returns without HTTP call."""
        with patch("blog.services.telegram.TELEGRAM_TOKEN", "foo"):
            response = send_message("Hello!")

        assert response["ok"] is True
        assert "skipped" in response["description"]
