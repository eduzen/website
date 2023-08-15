from http import HTTPStatus

import pytest
from django.test import SimpleTestCase


@pytest.mark.parametrize("url", ("media/test.jpg", "media"))
def test_media_view_not_found(client, url):
    response = client.get(url)
    assert response.status_code == 404


class FaviconTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/favicon.ico")

        assert response.status_code == HTTPStatus.OK
        assert response["Cache-Control"] == "max-age=86400, immutable, public"
        assert response["Content-Type"] == "image/svg+xml"
        assert response.content.startswith(b"<svg")
