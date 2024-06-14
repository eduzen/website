import unittest
from unittest.mock import Mock, patch

from requests.exceptions import HTTPError

from blog.services.telegram import send_message


class SendMessageTest(unittest.TestCase):
    # Happy path
    @patch("blog.services.telegram.requests.post")
    def test_send_message_success(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None  # This means no error
        mock_response.json.return_value = {"ok": True, "result": "Some response data"}

        mock_post.return_value = mock_response

        response = send_message("Hello!")

        assert response == {"ok": True, "result": "Some response data"}
        mock_post.assert_called_once()

    # Unhappy path
    @patch("blog.services.telegram.requests.post")
    def test_send_message_failure(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("An error occurred")

        mock_post.return_value = mock_response

        with self.assertRaises(HTTPError):
            send_message("Hello!")
        mock_post.assert_called_once()
