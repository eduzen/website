from django.contrib import admin

from .models import PublicImage


@admin.register(PublicImage)
class PublicImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image")
