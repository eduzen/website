import pytest
from django.urls import reverse


def test_root_admin(admin_client):
    admin_home_url = reverse("admin:index")
    response = admin_client.get(admin_home_url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "app",
    (
        "blog",
        "robots",
        "sessions",
        "sites",
        "snippets",
        "auth",
    ),
)
def test_installed_apps_admin(admin_client, app):
    response = admin_client.get(reverse("admin:app_list", kwargs={"app_label": app}))
    assert response.status_code == 200
