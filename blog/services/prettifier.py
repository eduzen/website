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
