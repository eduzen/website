from django.db import models

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    title = models.CharField(max_length=255, default='Site Name')
    subtitle = models.CharField(max_length=255, default='Subtitle Name')
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
