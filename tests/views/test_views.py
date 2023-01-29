import pytest


@pytest.mark.parametrize("url", ("media/test.jpg", "media"))
def test_media_view_not_found(client, url):
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.parametrize("url", ("favicon.ico",))
def test_media_view_not_found_faveicon(client, url):
    response = client.get(url)
    assert response.status_code == 404
