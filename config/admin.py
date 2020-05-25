from django.contrib import admin

from .models import BioConfiguration


@admin.register(BioConfiguration)
class BioConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle")
