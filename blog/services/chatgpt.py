import logging

import openai
from django.conf import settings

from blog.models import Post

logger = logging.getLogger(__name__)

openai.organization = settings.OPENAI_ORGANIZATION
openai.api_key = settings.OPENAI_API_KEY

gpt_models = {"3-5": "gpt-3.5-turbo-16k-0613", "3-5-16": "gpt-3.5-turbo-16k"}


def ask_openai(prompt: str) -> str:
    try:
        logger.debug(f"Sending prompt to chatgpt: {prompt}")
        response = openai.ChatCompletion.create(
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
        "I am writing my blog post. And I'm terrible with titles.\n"
        "I need your help improving my title. So the word title doesn't need to appear in the text.\n"
        "I need something also appealing to the reader and not serious.\n"
        "And it needs to create curiosity. The summary will be saved in a charfield in my db\n"
        "The max lengh is 200, but I would like to keep it shorter like 50 or 80.\n"
        f"The title of post is the following: '{title}'\n"
        "Please respect the language of the text and give only one suggested title.\n"
    )
    response = ask_openai(prompt)
    return response


def get_better_summary(text: str) -> str:
    prompt = (
        "I would like to improve the summary of my blog post.\n"
        "I need your help with a summary. So the word summary doesn't need to appear in the text.\n"
        "I need something also appealing to the reader and not serious.\n"
        "And it needs to create curiosity. The summary will be saved in a charfield in my db\n"
        "The max lengh is 300, but I would like to keep it around 200.\n"
        "Please respect the language of the text.\n"
        f"The content of the text of my post is the following text: {text}."
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
        post.suggestions = blog_post_suggestion(post)  # type: ignore
        post.save()
    except Exception as e:
        logger.error(f"Error improving post title for {post}: {e}")
