from unittest.mock import patch

import pytest
from pydantic import BaseModel

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
    def __init__(self, data):
        self.data = data


@pytest.fixture
def mock_agent_run_sync():
    with patch("blog.services.chatgpt.agent.run_sync") as mock_run_sync:
        mock_response_data = MockResponseData()
        mock_agent_response = MockAgentResponse(data=mock_response_data)
        mock_run_sync.return_value = mock_agent_response
        yield mock_run_sync


@pytest.fixture
def sample_post(db):
    return PostFactory.create(title="Original Title", text="Original content.", suggestions=None)


def test_get_better_title(mock_agent_run_sync):
    original_title = "Some Original Title"
    improved_title = get_better_title(original_title)

    assert improved_title == "Mocked Improved Title"
    mock_agent_run_sync.assert_called_once()


def test_get_better_summary(mock_agent_run_sync):
    original_text = "Some original blog post content."
    improved_summary = get_better_summary(original_text)

    assert improved_summary == "Mocked Improved Summary"
    mock_agent_run_sync.assert_called_once()


@patch("blog.services.chatgpt.get_better_title", return_value="Patched Title")
@patch("blog.services.chatgpt.get_better_summary", return_value="Patched Summary")
def test_blog_post_suggestion(mock_get_summary, mock_get_title, sample_post):
    suggestions = blog_post_suggestion(sample_post)

    assert suggestions == {"title": "Patched Title", "summary": "Patched Summary"}
    mock_get_title.assert_called_once_with(sample_post.title)
    mock_get_summary.assert_called_once_with(sample_post.text)


@patch("blog.services.chatgpt.blog_post_suggestion")
def test_improve_blog_post_success(mock_suggestion, sample_post):
    mock_suggestions = {"title": "Improved Title", "summary": "Improved Summary"}
    mock_suggestion.return_value = mock_suggestions

    improve_blog_post(sample_post)

    sample_post.refresh_from_db()
    assert sample_post.suggestions == mock_suggestions
    mock_suggestion.assert_called_once_with(sample_post)


@patch("blog.services.chatgpt.blog_post_suggestion", side_effect=Exception("AI Error"))
def test_improve_blog_post_failure(mock_suggestion, sample_post):
    with pytest.raises(Exception, match="AI Error"):
        improve_blog_post(sample_post)

    sample_post.refresh_from_db()
    assert sample_post.suggestions is None
    mock_suggestion.assert_called_once_with(sample_post)
