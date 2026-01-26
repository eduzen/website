from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted((item[1][0], item[0]) for item in LEXERS)
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default="python", max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
    highlighted = models.TextField(blank=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        Only re-highlights if code, language, style, linenos, or title changed.
        """
        # Check if we need to re-highlight
        should_highlight = True
        if self.pk:
            try:
                old = Snippet.objects.only("code", "language", "style", "linenos", "title").get(pk=self.pk)
                if (
                    old.code == self.code
                    and old.language == self.language
                    and old.style == self.style
                    and old.linenos == self.linenos
                    and old.title == self.title
                ):
                    should_highlight = False
            except Snippet.DoesNotExist:
                pass

        if should_highlight:
            lexer = get_lexer_by_name(self.language, stripall=True)
            linenos = "table" if self.linenos else False
            options = {"title": self.title} if self.title else {}
            formatter = HtmlFormatter(style=self.style, linenos=linenos, full=False, noclasses=True, **options)
            self.highlighted = highlight(self.code, lexer, formatter)

        super().save(*args, **kwargs)
