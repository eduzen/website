import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@pytest.mark.django_db
def test_snippet_highlight_view():
    # Arrange
    # Create a snippet with some highlighted content
    snippet = Snippet.objects.create(
        code="print('Hello, world!')", highlighted="<div class='highlighted'>print('Hello, world!')</div>"
    )

    client = APIClient()

    # Construct the URL for the highlight detail route
    # Assuming you have a router that registers SnippetViewSet as 'snippets'
    # The highlight action is detail=True, so URL pattern might look like:
    # /snippets/<id>/highlight/
    url = reverse("snippet-highlight", args=[snippet.id])

    # Act
    response = client.get(url, format="html")

    # Assert
    assert response.status_code == 200
    # Check that the response data is the snippet's highlighted attribute.
    # With StaticHTMLRenderer, response.data should be a string of HTML.
    assert response.content.decode("utf-8") == snippet.highlighted


@pytest.mark.django_db
def test_snippet_serializer():
    # Arrange
    snippet = Snippet.objects.create(
        title="Test snippet", code='print("Hello, World!")', linenos=True, language="python", style="friendly"
    )

    factory = APIRequestFactory()
    request = factory.get("/")
    serializer = SnippetSerializer(snippet, context={"request": request})

    # Act
    data = serializer.data

    # Assert that all expected fields are present
    expected_fields = {"url", "id", "title", "code", "linenos", "language", "style", "highlight"}
    assert expected_fields.issubset(data.keys())

    # Check that the highlight URL is correct
    expected_highlight_url = reverse("snippet-highlight", args=[snippet.id])
    assert data["highlight"].endswith(expected_highlight_url)

    # Validate the snippet fields match what we created
    assert data["title"] == "Test snippet"
    assert data["code"] == 'print("Hello, World!")'
    assert data["linenos"] is True
    assert data["language"] == "python"
    assert data["style"] == "friendly"
