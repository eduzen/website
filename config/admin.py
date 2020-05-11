from django.contrib import admin

from .models import BioConfiguration, ContactConfiguration, SiteConfiguration, TwitterConfiguration


@admin.register(BioConfiguration)
class BioConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle")


@admin.register(ContactConfiguration)
class ContactConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle", "body")


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle", "tab_title", "home", "url_linkedin", "url_github", "url_twitter")


@admin.register(TwitterConfiguration)
class TwitterConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "consumer_key", "consumer_secret", "access_token", "access_token_secret")
