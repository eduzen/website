from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import QuerySet
from django.forms import Textarea, TextInput
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin

from blog.services.parsers import json_to_pretty_html

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
    empty_value_display = "-"
    search_fields = ["text", "title", "slug", "summary"]
    list_display = [
        "created_date",
        "published",
        "title",
        "blog_link",
        "slug",
        "published_date",
        "preview",
        "tag_list",
    ]
    list_display_links = ("title",)
    readonly_fields = (
        "preview",
        "pk",
        "raw_body",
        "improve_button",
        "blog_link",
        "apply_styles",
        "suggested_title",
        "suggested_summary",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "200"})},
        models.JSONField: {"widget": Textarea(attrs={"rows": 8, "cols": 200})},
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("author", "created_date"),
                    "title",
                    "blog_link",
                    "summary",
                    "slug",
                    ("published_date", "apply_styles"),
                    "text",
                    ("image", "preview"),
                    "cropping",
                )
            },
        ),
        (
            "Suggestions",
            {
                "classes": ("collapse",),
                "fields": (
                    "suggested_title",
                    "suggested_summary",
                    "suggestions",
                    "improve_button",
                ),
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),  # This will make the fieldset collapsible
                "fields": ("tags", "raw_body"),
            },
        ),
    )

    class Meta:
        js = ("blog/js/htmx.min.1.9.4.js",)

    @admin.display(description="Suggested Title")
    def suggested_title(self, obj: Post) -> str:
        return obj.suggestions.get("title", "") if obj.suggestions else ""

    @admin.display(description="Suggested Summary")
    def suggested_summary(self, obj: Post) -> str:
        return obj.suggestions.get("summary", "") if obj.suggestions else ""

    @admin.display(boolean=True)
    def published(self, obj: Post):
        return obj.published

    @mark_safe
    def preview(self, obj: Post) -> str:
        if not obj.image:
            return ""
        return f"<img src='{obj.image.url}' width='100' height='100'/>"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Post]:
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj: Post):
        return ", ".join(o.word for o in obj.tags.all())

    @mark_safe
    def raw_body(self, obj: Post) -> str:
        return obj.text

    def blog_link(self, obj: Post) -> str:
        if not obj.published:
            return "-"
        return mark_safe(f"<a href='{obj.get_absolute_url()}'>Go to eduzen.ar</a>")

    @mark_safe
    def apply_styles(self, post: Post) -> str:
        if not post.pk:
            return "-"

        url = reverse("post_update_styles", kwargs={"post_id": post.pk})
        return f"<a href='{url}' class='button' style='background-color:green'> apply </a>"

    @mark_safe
    def improve_button(self, obj: Post) -> str:
        if not obj.pk:
            return "-"
        context = {"post_id": obj.pk}
        return render_to_string("blog/admin/partials/improve_button.html", context)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "slug")
    search_fields = ("slug",)
    prepopulated_fields = {"slug": ("word",)}
