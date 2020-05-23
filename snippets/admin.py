from django.contrib import admin
from django.utils.html import mark_safe
from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "title",
        "code",
        "linenos",
        "language",
        "style",
    )
    list_filter = ("created", "linenos")
    readonly_fields = ("highlighted", "pretty", "created", "id")

    fields = (
        "id",
        "created",
        "title",
        "code",
        "linenos",
        "language",
        "style",
        "pretty",
    )

    @mark_safe
    def pretty(self, obj):
        return obj.highlighted
