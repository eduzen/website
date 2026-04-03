# Wrap heavy Pygments introspection in cache so it runs once per
# process on first access rather than at every import / worker startup.
from collections.abc import Collection, Iterable
from functools import cache

from django.db import models
from django.db.models.base import ModelBase
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


@cache
def get_language_choices() -> list[tuple[str, str]]:
    """Return sorted (value, label) pairs for all Pygments lexers — cached."""
    return sorted((item[1][0], item[0]) for item in get_all_lexers() if item[1])


@cache
def get_style_choices() -> list[tuple[str, str]]:
    """Return sorted (value, label) pairs for all Pygments styles — cached."""
    return sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=get_language_choices, default="python", max_length=100)
    style = models.CharField(choices=get_style_choices, default="friendly", max_length=100)
    highlighted = models.TextField(blank=True)

    class Meta:
        ordering = ["created"]

    def __str__(self) -> str:
        return self.title or ""

    def save(
        self,
        *,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.

        Instead of querying the old row to detect changes (which adds
        an extra SELECT on every save), we rely on `update_fields` when it is
        supplied.  If the caller only saves unrelated fields (e.g. just
        `save(update_fields=["title"])` for a non-highlight field) we skip re-
        highlighting.  For full saves we always re-highlight to stay correct.
        """
        _HIGHLIGHT_FIELDS = {"code", "language", "style", "linenos", "title"}
        normalized_update_fields: set[str] | None = None
        if isinstance(update_fields, Collection) and not isinstance(update_fields, str):
            normalized_update_fields = {field for field in update_fields if isinstance(field, str)}

        should_highlight = (
            # Full save (no update_fields hint) — re-highlight to be safe
            normalized_update_fields is None
            # Partial save that touches at least one highlight-affecting field
            or bool(_HIGHLIGHT_FIELDS & normalized_update_fields)
            # New record or somehow lost the cached value
            or not self.highlighted
        )

        if should_highlight:
            lexer = get_lexer_by_name(self.language, stripall=True)
            linenos = "table" if self.linenos else False
            options = {"title": self.title} if self.title else {}
            formatter = HtmlFormatter(  # type: ignore[call-overload]
                style=self.style,
                linenos=linenos,
                full=False,
                noclasses=True,
                **options,
            )
            self.highlighted = highlight(self.code, lexer, formatter)
            if normalized_update_fields is not None:
                update_fields = sorted({*normalized_update_fields, "highlighted"})

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
