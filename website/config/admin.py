from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import SiteConfiguration, TwitterConfiguration

# Register your models here.
admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(TwitterConfiguration, SingletonModelAdmin)
