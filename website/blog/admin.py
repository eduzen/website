# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Post
from .models import Tag
from .models import CustomPage


class PostAdmin(admin.ModelAdmin):

    search_fields = ["author", "title", "published_date"]

    list_filter = ["author", "title", "published_date"]

    list_display = ["author", "title", "published_date"]


class CustomPageAdmin(admin.ModelAdmin):

    search_fields = ["name"]

    list_filter = ["name"]

    list_display = ["name", "slug"]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(CustomPage, CustomPageAdmin)
