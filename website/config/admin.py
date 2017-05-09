from django.contrib import admin

from solo.admin import SingletonModelAdmin
from djangoseo.admin import register_seo_admin

from .models import SiteConfiguration, TwitterConfiguration
from .models import MyMetadata


# Register your models here.
admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(TwitterConfiguration, SingletonModelAdmin)
register_seo_admin(admin.site, MyMetadata)

