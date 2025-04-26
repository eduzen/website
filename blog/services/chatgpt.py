# blog/services/chatgpt.py
from typing import Any, cast

import logfire
from django.conf import settings
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName

from blog.models import Post


class TitleSummaryModel(BaseModel):
    title: str
    summary: str


model = cast(KnownModelName, settings.PYDANTIC_AI_MODEL)
agent: Agent[Any, TitleSummaryModel] | None = None


def _get_agent() -> Agent[Any, TitleSummaryModel]:
    """Initializes and returns the Pydantic AI Agent."""
    global agent
    if agent is None:
        agent = Agent(model, output_type=TitleSummaryModel)
    return agent


def get_better_title(title: str) -> str:
    """
    Returns a single improved title for the given blog post title
    using pydantic-ai + OpenAI (GPT-4 or whichever you've set).
    """
    current_agent = _get_agent()
    prompt = (
        "Given the language and context of the following title, provide a captivating and "
        "improved title that will intrigue readers. Not too serious. "
        "Constraints:\n"
        "    - The word 'title' doesn't need to appear.\n"
        "    - I need only one suggested title.\n"
        "    - The max length is 200, ideally shorter (50–80).\n"
        "    - Please respect the language of the text.\n"
        "If it is Spanish, respond in Spanish. If English, respond in English.\n"
        f"Title: '{title}'"
    )

    logfire.debug(f"Asking pydantic-ai for an improved title:\n{prompt}")
    try:
        response = current_agent.run_sync(prompt)
        improved_title = response.data.title
        logfire.debug(f"Improved title: {improved_title}")
    except Exception as e:
        logfire.error(f"Error getting improved title: {e}")
        raise
    return improved_title


def get_better_summary(text: str) -> str:
    """
    Returns a single improved summary for the given blog post content
    using pydantic-ai + OpenAI.
    """
    current_agent = _get_agent()
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

    logfire.debug(f"Asking pydantic-ai for an improved summary:\n{prompt}")
    response = current_agent.run_sync(prompt)
    improved_summary = response.data.summary
    logfire.debug(f"Improved summary: {improved_summary}")
    return improved_summary


def blog_post_suggestion(post: Post) -> dict[str, str]:
    """
    Generates a new title and summary for the given Post model instance
    and returns them as a dictionary.
    """
    title = get_better_title(post.title)
    summary = get_better_summary(post.text)
    return {"title": title, "summary": summary}


def improve_blog_post(post: Post) -> None:
    """
    Improves the post title and summary using pydantic-ai,
    then updates the 'suggestions' field (assuming your model can store it).
    """
    try:
        suggestions = blog_post_suggestion(post)
        Post.objects.filter(id=post.id).update(suggestions=suggestions)
    except Exception as e:
        logfire.error(f"Error improving post title for {post}: {e}")
        raise
