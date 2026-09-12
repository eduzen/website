from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

from blog.models import Post
from blog.services.chatgpt import (
    OpenAINotConfiguredError,
    TitleSummaryModel,
    _get_agent,
    blog_post_suggestion,
    get_better_summary,
    get_better_title,
    improve_blog_post,
)
from blog.tests.factories import PostFactory


@pytest.fixture
def mock_agent_run_sync() -> Iterator[MagicMock]:
    mock_agent = MagicMock()
    mock_agent.run_sync.return_value = MagicMock(
        output=TitleSummaryModel(title="Mocked Improved Title", summary="Mocked Improved Summary")
    )
    with patch("blog.services.chatgpt._get_agent", return_value=mock_agent):
        yield mock_agent


@pytest.fixture
def sample_post(db: None) -> Post:
    del db
    return PostFactory.create(title="Original Title", text="Original content.", suggestions=None)


def test_get_better_title(mock_agent_run_sync: MagicMock) -> None:
    improved_title = get_better_title("Some Original Title")

    assert improved_title == "Mocked Improved Title"
    mock_agent_run_sync.run_sync.assert_called_once()


def test_get_better_summary(mock_agent_run_sync: MagicMock) -> None:
    improved_summary = get_better_summary("Some original blog post content.")

    assert improved_summary == "Mocked Improved Summary"
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


def test_get_agent_raises_when_openai_not_configured() -> None:
    with (
        patch("blog.services.chatgpt.settings.OPENAI_API_KEY", ""),
        pytest.raises(OpenAINotConfiguredError),
    ):
        _get_agent()
