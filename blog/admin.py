from django.contrib import admin
from django.forms import TextInput, ModelForm
from django.db import models

from .models import Post
from .models import Comment
from .models import Tag
from .models import CustomPage
from .models import DolarPeso


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    search_fields = ["author", "title", "published", "published_date", "created_date"]
    list_filter = ["published_date", "author", "title", "created_date"]
    list_display = ["published", "author", "title", "slug", "created_date", "published_date", "image_tag", "tag_list"]
    list_display_links = ("title", "author")
    readonly_fields = ("image_tag",)

    formfield_overrides = {models.CharField: {"widget": TextInput(attrs={"size": "130"})}}
    filter_horizontal = ("tags",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.word for o in obj.tags.all())


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ["author", "created_date", "approved_comment"]
    list_filter = ["author", "created_date", "approved_comment"]
    list_display = ["author", "post", "created_date", "approved_comment"]


@admin.register(DolarPeso)
class DolarPesoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'balance_currency',
        'balance',
        'name',
        'bid_currency',
        'bid',
        'ask_currency',
        'ask',
        'rate_currency',
        'rate',
        'created_date',
    )
    list_filter = ('created_date',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'slug')
    search_fields = ('slug',)


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'include_header', 'include_footer', 'include_contact_form', 'content')
    list_filter = ('include_header', 'include_footer', 'include_contact_form')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
