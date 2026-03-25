from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from blog.models import Post
from blog.services.chatgpt import (
    blog_post_suggestion,
    get_better_summary,
    get_better_title,
    improve_blog_post,
)
from blog.tests.factories import PostFactory


class MockResponseData(BaseModel):
    title: str = "Mocked Improved Title"
    summary: str = "Mocked Improved Summary"


class MockAgentResponse:
    def __init__(self, data: MockResponseData) -> None:
        self.output = data


@pytest.fixture
def mock_agent_run_sync() -> Iterator[MagicMock]:
    mock_response_data = MockResponseData()
    mock_agent_response = MockAgentResponse(data=mock_response_data)

    # Create a mock agent with a mock run_sync method
    mock_agent = MagicMock()
    mock_agent.run_sync.return_value = mock_agent_response

    # Patch _get_agent to return our mock agent
    with patch("blog.services.chatgpt._get_agent", return_value=mock_agent):
        yield mock_agent  # Yield the mock agent itself for assertions


@pytest.fixture
def sample_post(db: None) -> Post:
    del db
    return PostFactory.create(title="Original Title", text="Original content.", suggestions=None)


def test_get_better_title(mock_agent_run_sync: MagicMock) -> None:
    original_title = "Some Original Title"
    improved_title = get_better_title(original_title)

    assert improved_title == "Mocked Improved Title"
    # Assert run_sync was called on the mock agent returned by the patched _get_agent
    mock_agent_run_sync.run_sync.assert_called_once()


def test_get_better_summary(mock_agent_run_sync: MagicMock) -> None:
    original_text = "Some original blog post content."
    improved_summary = get_better_summary(original_text)

    assert improved_summary == "Mocked Improved Summary"
    # Assert run_sync was called on the mock agent returned by the patched _get_agent
    mock_agent_run_sync.run_sync.assert_called_once()


def test_blog_post_suggestion(mock_agent_run_sync: MagicMock, sample_post: Post) -> None:
    suggestions = blog_post_suggestion(sample_post)

    assert suggestions == {
        "title": "Mocked Improved Title",
        "summary": "Mocked Improved Summary",
    }
    mock_agent_run_sync.run_sync.assert_called_once()


@patch("blog.services.chatgpt.blog_post_suggestion")
def test_improve_blog_post_success(mock_suggestion: MagicMock, sample_post: Post) -> None:
    mock_suggestions = {"title": "Improved Title", "summary": "Improved Summary"}
    mock_suggestion.return_value = mock_suggestions

    improve_blog_post(sample_post)

    sample_post.refresh_from_db()
    assert sample_post.suggestions == mock_suggestions
    mock_suggestion.assert_called_once_with(sample_post)


@patch("blog.services.chatgpt.blog_post_suggestion", side_effect=Exception("AI Error"))
def test_improve_blog_post_failure(mock_suggestion: MagicMock, sample_post: Post) -> None:
    with pytest.raises(Exception, match="AI Error"):
        improve_blog_post(sample_post)

    sample_post.refresh_from_db()
    assert sample_post.suggestions is None
    mock_suggestion.assert_called_once_with(sample_post)
