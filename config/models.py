# -*- coding: utf-8 -*-
from django.db import models

from solo.models import SingletonModel
from ckeditor_uploader.fields import RichTextUploadingField


class BioConfiguration(SingletonModel):
    title = models.CharField(max_length=255, default="Quién les escribe")
    subtitle = models.CharField(max_length=255, blank=True)
    small = RichTextUploadingField(null=True, blank=True)
    long = RichTextUploadingField(null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    bio_pic = models.ImageField(null=True, upload_to="bio-pic/%Y/%m/%d", )
    pic_0 = models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d", )
    pic_1 = models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d", )
    pic_2 = models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d", )

    def __str__(self):
        return "Pagina de Bio/About"

    class Meta:
        verbose_name = "Bio/About configuration"


class ContactConfiguration(SingletonModel):
    title = models.CharField(max_length=255, default="Contacto")
    subtitle = models.CharField(max_length=255, blank=True)
    body = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return "Contact config"

    class Meta:
        verbose_name = "Contact configuration"


class SiteConfiguration(SingletonModel):
    title = models.CharField(max_length=255, default="Site Name")
    subtitle = models.CharField(max_length=255, default="Subtitle Name")
    tab_title = models.CharField(max_length=255, default="Tab title")
    home = models.URLField(max_length=500, default="eduardoenriquez.com.ar")
    url_linkedin = models.URLField(max_length=500, default="linkedin")
    url_github = models.URLField(max_length=500, default="github")
    url_twitter = models.URLField(max_length=500, default="twitter")

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class TwitterConfiguration(SingletonModel):
    consumer_key = models.CharField(max_length=255, default="consumer key")
    consumer_secret = models.CharField(max_length=255, default="consumer secret")
    access_token = models.CharField(max_length=255, default="access token")
    access_token_secret = models.CharField(max_length=255, default="access token secret")

    @property
    def data(self):
        response = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
            "access_token_key": self.access_token,
            "access_token_secret": self.access_token_secret,
        }
        return response

    def __str__(self):
        return "Twitter api Configuration"

    class Meta:
        verbose_name = "Twitter api Configuration"
