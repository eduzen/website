import json

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db import models
from django.forms import TextInput
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

from .models import Post, Tag


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def data_prettified(self, data):
        """Function to display pretty version of our data"""
        response = json.dumps(data, sort_keys=True, indent=2)
        formatter = HtmlFormatter(style="colorful")
        response = highlight(response, JsonLexer(), formatter)
        style = f"<style>{formatter.get_style_defs()}</style><br>"
        return mark_safe(style + response)

    def _session_data(self, obj):
        data = obj.get_decoded()
        if not data:
            return {}
        return self.data_prettified(data)

    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]
    exclude = ["session_data"]
    date_hierarchy = "expire_date"


@admin.register(Post)
class PostAdmin(ImageCroppingMixin, admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "unknown"
    search_fields = ["text", "title", "slug", "pompadour"]
    list_display = ["published", "author", "title", "slug", "created_date", "published_date", "preview", "tag_list"]
    list_display_links = ("title", "author")
    readonly_fields = ("preview", "pk")
    prepopulated_fields = {"slug": ("title",)}

    fields = [
        (
            "author",
            "created_date",
        ),
        "title",
        "pompadour",
        "slug",
        "published_date",
        "tags",
        "text",
        (
            "image",
            "preview",
        ),
        "cropping",
    ]
    formfield_overrides = {models.CharField: {"widget": TextInput(attrs={"size": "130"})}}
    filter_horizontal = ("tags",)

    @admin.display(boolean=True)
    def published(self, obj: Post):
        return obj.published

    @mark_safe
    def preview(self, obj):
        if not obj.image:
            return ""
        return f"<img src='{obj.image.url}' width='100' height='100'/>"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.word for o in obj.tags.all())


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "slug")
    search_fields = ("slug",)
    prepopulated_fields = {"slug": ("word",)}
