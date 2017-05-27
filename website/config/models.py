# -*- coding: utf-8 -*-
from django.db import models

from solo.models import SingletonModel
from djangoseo import seo
from ckeditor_uploader.fields import RichTextUploadingField


class BioConfiguration(SingletonModel):
    title = models.CharField(
        max_length=255, default="Quién les escribe"
    )
    subtitle = models.CharField(
        max_length=255, null=True, blank=True
    )
    body = RichTextUploadingField(null=True, blank=True)

    def __unicode__(self):
        return u"Pagina de Bio/About"

    class Meta:
        verbose_name = "Bio/About configuration"


class ContactConfiguration(SingletonModel):
    title = models.CharField(
        max_length=255, default="Contacto"
    )
    subtitle = models.CharField(
        max_length=255, null=True, blank=True
    )
    body = RichTextUploadingField(null=True, blank=True)

    def __unicode__(self):
        return u"Contact config"

    class Meta:
        verbose_name = "Contact configuration"


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


class TwitterConfiguration(SingletonModel):
    consumer_key = models.CharField(max_length=255, default='consumer key')
    consumer_secret = models.CharField(max_length=255, default='consumer secret')
    access_token = models.CharField(max_length=255, default='access token')
    access_token_secret = models.CharField(max_length=255, default='access token secret')

    @property
    def data(self):
        response = {
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'access_token_key': self.access_token,
            'access_token_secret': self.access_token_secret,
        }
        return  response

    def __unicode__(self):
        return u"Twitter api Configuration"

    class Meta:
        verbose_name = "Twitter api Configuration"


class MyMetadata(seo.Metadata):
    title = seo.Tag(head=True, max_length=68)
    description = seo.MetaTag(max_length=155)
    keywords = seo.KeywordTag()
    heading = seo.Tag(name="h1")

