# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField


class Tag(models.Model):
    word = models.CharField(max_length=50)
    slug = models.CharField(max_length=250)

    def __unicode__(self):
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
    slug = AutoSlugField(
        editable=True, null=True, blank=True, unique=True,
        populate_from='title', verbose_name=u"Url"
    )
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    text = RichTextUploadingField(verbose_name=u"Cuerpo de texto")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    @models.permalink
    def get_absolute_url(self):
        return 'blog:post', (self.slug,)

    def __unicode__(self):
        return u"{}".format(self.title)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class CustomPage(models.Model):
    name = models.CharField(
        verbose_name=u"Nombre", max_length=250)

    slug = AutoSlugField(
        populate_from='name'
    )

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

    @models.permalink
    def get_absolute_url(self):
        return 'blog:post', (self.slug,)

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = "Páginas custom"
        verbose_name_plural = u"Páginas custom"
