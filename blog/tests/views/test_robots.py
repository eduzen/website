from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestRobot(TestCase):
    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        assert response.status_code == HTTPStatus.OK
        assert response["Content-Type"] == "text/plain"

    def test_robots_list_txt(self):
        response = self.client.get(reverse("robots_rule_list"))
        assert response.status_code == HTTPStatus.OK
        assert response["Content-Type"] == "text/plain"
