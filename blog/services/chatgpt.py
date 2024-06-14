import logging

from django.conf import settings
from openai import OpenAI

from blog.models import Post

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    organization=settings.OPENAI_ORGANIZATION,
)

gpt_models = {"3-5": "gpt-3.5-turbo-16k-0613", "3-5-16": "gpt-3.5-turbo-16k"}


def ask_openai(prompt: str) -> str:
    try:
        logger.debug(f"Sending prompt to chatgpt: {prompt}")
        response = client.chat.completions.create(
            model=gpt_models["3-5-16"], messages=[{"role": "user", "content": prompt}]
        )
        content = response["choices"][0]["message"]["content"].replace('"', "")  # type: ignore
        logger.debug(f"Chatgpt answer: {content}")
        return content
    except Exception as e:
        logger.error(f"Error asking chatgpt: {e}")
        raise


def get_better_title(title: str) -> str:
    prompt = (
        "Given the language and context of the following title, provide a captivating and"
        "improved title that will intrigue readers. Not too serious."
        "Constrains:"
        "    - The word title doesn't need to appear in the text.\n"
        "    - I need only one suggested title.\n"
        "    - The max length is 200, but I would like to keep it shorter like 50 or 80.\n"
        "    - Please respect the language of the text."
        "    If it is in spanish, give me a title in spanish\n"
        "    If it's english, give me a title in english.\n"
        f"The title of my blog post is: '{title}'."
    )

    response = ask_openai(prompt)
    return response


def get_better_summary(text: str) -> str:
    prompt = (
        "Given the language and context of the following blog post content,"
        " provide a concise and intriguing summary that captures its essence. "
        f"The content of my blog post is: '{text}'."
        "Constrains:"
        "1) the word summary doesn't need to appear in the text.\n"
        "2) The max length is 300, but I would like to keep it around 200.\n"
        "3) Please respect the language of the text."
        " If it is in spanish, give me a summary in spanish\n"
        " If it's english, give me a summary in english.\n"
        "4) Only one summary is needed.\n"
    )
    response = ask_openai(prompt)
    return response


def blog_post_suggestion(post: Post) -> dict[str, str]:
    title = get_better_title(post.title)
    summary = get_better_summary(post.text)

    return {"title": title, "summary": summary}


def improve_blog_post(post: Post) -> None:
    """
    Improve the post title and summary using chatgpt.
    """
    try:
        suggestions = blog_post_suggestion(post)  # type: ignore
        Post.objects.filter(id=post.pk).update(suggestions=suggestions)
    except Exception as e:
        logger.error(f"Error improving post title for {post}: {e}")
