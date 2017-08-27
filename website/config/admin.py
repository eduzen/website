from django.contrib.admin.models import LogEntry
from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import SiteConfiguration, TwitterConfiguration
from .models import BioConfiguration, ContactConfiguration

# Register your models here.
admin.site.register(LogEntry)
admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(TwitterConfiguration, SingletonModelAdmin)
admin.site.register(BioConfiguration, SingletonModelAdmin)
admin.site.register(ContactConfiguration, SingletonModelAdmin)
