import functools
import logging
from typing import Any, cast

from django.conf import settings
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName

from blog.models import Post

logger = logging.getLogger(__name__)


class TitleSummaryModel(BaseModel):
    title: str
    summary: str


class OpenAINotConfiguredError(RuntimeError):
    """Raised when OpenAI API key is not configured."""

    def __init__(self) -> None:
        super().__init__("OPENAI_API_KEY is not configured. Set it to enable AI post improvements.")


@functools.cache
def _build_agent() -> Agent[Any, TitleSummaryModel]:
    model = cast(KnownModelName, settings.PYDANTIC_AI_MODEL)
    return Agent(model, output_type=TitleSummaryModel)


def _get_agent() -> Agent[Any, TitleSummaryModel]:
    if not settings.OPENAI_API_KEY:
        raise OpenAINotConfiguredError()
    return _build_agent()


def _run_prompt(prompt: str) -> TitleSummaryModel:
    logger.debug("Asking pydantic-ai:\n%s", prompt)
    return _get_agent().run_sync(prompt).output


def get_better_title(title: str) -> str:
    """
    Returns a single improved title for the given blog post title
    using pydantic-ai + OpenAI (GPT-4 or whichever you've set).
    """
    prompt = (
        "Given the language and context of the following title, provide a captivating and "
        "improved title that will intrigue readers. Not too serious.\n"
        "Constraints:\n"
        "1) The word 'title' doesn't need to appear.\n"
        "2) I need only one suggested title.\n"
        "3) The max length is 200, ideally shorter (50-80).\n"
        "4) Please respect the language of the text.\n"
        "If it is Spanish, respond in Spanish. If English, respond in English.\n"
        f"Title: '{title}'"
    )
    return _run_prompt(prompt).title


def get_better_summary(text: str) -> str:
    """
    Returns a single improved summary for the given blog post content
    using pydantic-ai + OpenAI.
    """
    prompt = (
        "Given the language and context of the following blog post content, "
        "provide a concise and intriguing summary that captures its essence.\n"
        "Constraints:\n"
        "1) The word 'summary' doesn't need to appear.\n"
        "2) The max length is 300, ideally ~200.\n"
        "3) Respect the language of the text: if Spanish, respond in Spanish; if English, in English.\n"
        "4) Only one summary is needed.\n"
        f"Content: '{text}'"
    )
    return _run_prompt(prompt).summary


def blog_post_suggestion(post: Post) -> dict[str, str]:
    """
    Generates a new title and summary for the given Post model instance
    and returns them as a dictionary.
    """
    prompt = (
        "Given the language and context of the following blog post, provide both:\n"
        "1) a captivating improved title, not too serious\n"
        "2) a concise and intriguing summary\n"
        "Constraints:\n"
        "1) Respect the language of the text: if Spanish, respond in Spanish; if English, in English.\n"
        "2) Return exactly one title and one summary.\n"
        "3) The title should be shorter than 200 characters, ideally 50-80.\n"
        "4) The summary should be shorter than 300 characters, ideally around 200.\n"
        f"Current title: '{post.title}'\n"
        f"Content: '{post.text}'"
    )
    output = _run_prompt(prompt)
    return {"title": output.title, "summary": output.summary}


def improve_blog_post(post: Post) -> None:
    """
    Improves the post title and summary using pydantic-ai,
    then updates the 'suggestions' field (assuming your model can store it).
    """
    try:
        suggestions = blog_post_suggestion(post)
        Post.objects.filter(id=post.id).update(suggestions=suggestions)
    except Exception:
        logger.exception("Error improving post %s", post)
        raise
