# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField


class Tag(models.Model):
    word = models.CharField(max_length=50)
    slug = models.CharField(max_length=250)

    def __unicode__(self):
        return u"{}".format(self.slug)

    def __str__(self):
        return u"{}".format(self.slug)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(
        max_length=200, verbose_name=u"Titulo"
    )
    pompadour = models.CharField(
        max_length=800, null=True, blank=True,
        verbose_name=u"Resumen para portada"
    )
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    text = RichTextUploadingField(verbose_name=u"Cuerpo de texto")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return u"{}".format(self.title)


class CustomPage(models.Model):
    name = models.CharField(
        verbose_name=u"Nombre", max_length=250)

    slug = models.CharField(
        verbose_name=u"Url", max_length=250)

    include_header = models.BooleanField(
        default=True, verbose_name=u"Incluir header"
    )

    include_footer = models.BooleanField(
        default=True, verbose_name=u"Incluir footer"
    )

    include_contact_form = models.BooleanField(
        default=True, verbose_name=u"Incluir formulario de contacto"
    )

    content = RichTextUploadingField(
        verbose_name=u"Contenido", null=True, blank=True
    )

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = "Páginas custom"
        verbose_name_plural = u"Páginas custom"
