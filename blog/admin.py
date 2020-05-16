from django.contrib import admin
from django.db import models
from django.forms import TextInput

from .models import Comment, DolarPeso, Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    search_fields = ["text", "title", "slug", "pompadour"]
    list_filter = ["published_date", "created_date"]
    list_display = ["published", "author", "title", "slug", "created_date", "published_date", "image_tag", "tag_list"]
    list_display_links = ("title", "author")
    readonly_fields = ("image_tag", "pk")

    fields = [
        ("author", "created_date",),
        "title",
        "pompadour",
        "slug",
        "published_date",
        "tags",
        "text",
        "image",
        "image_tag",
    ]
    formfield_overrides = {models.CharField: {"widget": TextInput(attrs={"size": "130"})}}
    filter_horizontal = ("tags",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.word for o in obj.tags.all())


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ["author", "created_date", "approved_comment"]
    list_filter = ["author", "created_date", "approved_comment"]
    list_display = ["author", "post", "created_date", "approved_comment"]


@admin.register(DolarPeso)
class DolarPesoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "balance_currency",
        "balance",
        "name",
        "bid_currency",
        "bid",
        "ask_currency",
        "ask",
        "rate_currency",
        "rate",
        "created_date",
    )
    list_filter = ("created_date",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "slug")
    search_fields = ("slug",)
