from bs4 import BeautifulSoup, Tag
import json
from typing import Any
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer


def json_to_pretty_html(data: dict[str, Any]) -> str:
    """Function to display pretty version of our data"""
    if not data:
        return "No data"

    response = json.dumps(data, sort_keys=True, indent=2)
    formatter = HtmlFormatter(style="colorful")
    response = highlight(response, JsonLexer(), formatter)
    result = f"<style>{formatter.get_style_defs()}</style><br>{response}"
    return result.strip()


def clear_all_styles(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(True):  # find_all(True) returns all tags in the soup
        tag.attrs.pop("class", None)  # Remove the class attribute
        tag.attrs.pop("style", None)  # Remove the inline style attribute
        # Add more attributes here if you wish to reset others


def apply_styles(content: str) -> str:
    """
    Apply specific styles to HTML content using BeautifulSoup.

    :param content: HTML content string
    :return: styled HTML content string
    """
    soup = BeautifulSoup(content, "html.parser")

    # Clear all existing styles
    clear_all_styles(soup)

    # Update <h2> tags
    _style_h2_tags(soup.find_all("h2"))

    # Update <p> tags
    _style_p_tags(soup.find_all("p"))

    # Update <pre><code> tags
    _style_pre_tags(soup, soup.find_all("pre"))

    return str(soup)


def _style_h2_tags(tags: list[Tag]) -> None:
    for tag in tags:
        tag["class"] = "text-yellow-400 mt-8 text-3xl font-bold mb-6 text-left"


def _style_p_tags(tags: list[Tag]) -> None:
    for tag in tags:
        tag["class"] = "text-xl mt-4 leading-relaxed text-justify"


def _style_pre_tags(soup: BeautifulSoup, tags: list[Tag]) -> None:
    for tag in tags:
        tag["class"] = "relative bg-white text-black n p-6 rounded-lg"

        # Adding the copy button as a child to each <pre> tag
        copy_button = soup.new_tag(
            "button",
            **{
                "class": "copy-btn absolute top-2 right-2 bg-blue-600 text-white px-2 py-1 "
                "rounded transition duration-300"
            },
        )
        copy_button.string = "Copy"
        tag.append(copy_button)
