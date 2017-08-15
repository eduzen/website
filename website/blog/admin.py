# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from .models import Post
from .models import Comment
from .models import Tag
from .models import CustomPage
from .models import DolarPeso

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'

    search_fields = ["author", "title", "published_date", "created_date"]

    list_filter = ["author", "title", "published_date", "created_date"]

    list_display = ["author", "title", "slug", "published_date", "created_date"]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100',})},
    }


class CommentAdmin(admin.ModelAdmin):

    search_fields = [
        "author", "created_date", "approved_comment"
    ]

    list_filter = ["author", "created_date", "approved_comment"]

    list_display = [
        "author", "post", "created_date", "approved_comment"
    ]


class CustomPageAdmin(admin.ModelAdmin):

    search_fields = ["name"]

    list_filter = ["name"]

    list_display = ["name", "slug"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(DolarPeso)
admin.site.register(CustomPage, CustomPageAdmin)
