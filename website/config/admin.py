from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import SiteConfiguration

# Register your models here.
admin.site.register(SiteConfiguration, SingletonModelAdmin)
