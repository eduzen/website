from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer


def highlight_json(json_data: str) -> str:
    """Formats and highlights a JSON string for HTML presentation."""
    formatter = HtmlFormatter(style="colorful")
    highlighted_data = highlight(json_data, JsonLexer(), formatter)

    custom_styles = """
    pre {
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 70%;  /* Optional: set a max width if desired */
    }
    """

    return f"<style>{formatter.get_style_defs()}{custom_styles}</style><br>{highlighted_data}"
