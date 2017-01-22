from django.db import models

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    title = models.CharField(max_length=255, default='Site Name')
    subtitle = models.CharField(max_length=255, default='Subtitle Name')
    tab_title = models.CharField(max_length=255, default='Tab title')
    home = models.URLField(max_length=500, default='eduardoenriquez.com.ar')
    url_linkedin = models.URLField(max_length=500, default='linkedin')
    url_github = models.URLField(max_length=500, default='github')
    url_twitter = models.URLField(max_length=500, default='twitter')

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
