from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db import models
from django.forms import TextInput
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from blog.services.prettifier import json_to_pretty_html

from .models import Post, Tag


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]
    exclude = ["session_data"]
    date_hierarchy = "expire_date"

    @mark_safe
    def _session_data(self, obj: Session):
        return json_to_pretty_html(obj.get_decoded())


@admin.register(Post)
class PostAdmin(ImageCroppingMixin, admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "unknown"
    search_fields = ["text", "title", "slug", "summary"]
    list_display = [
        "published",
        "link",
        "author",
        "title",
        "slug",
        "created_date",
        "published_date",
        "preview",
        "tag_list",
    ]
    list_display_links = ("title", "author")
    readonly_fields = ("preview", "pk", "raw_body")
    prepopulated_fields = {"slug": ("title",)}

    fields = [
        (
            "author",
            "created_date",
        ),
        "title",
        "summary",
        "slug",
        "published_date",
        "tags",
        "text",
        "raw_body",
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

    def raw_body(self, obj):
        return obj.text

    def link(self, obj):
        return mark_safe(f"<a href='{obj.get_absolute_url()}'>link</a>")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "slug")
    search_fields = ("slug",)
    prepopulated_fields = {"slug": ("word",)}
