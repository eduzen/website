# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from djmoney.models.fields import MoneyField


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

    def published(self):
        return True if self.published_date else False

    published.boolean = True
    published.short_description = 'Published'

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    @models.permalink
    def get_absolute_url(self):
        return 'blog:post', (self.slug,)

    def __unicode__(self):
        return u"{}".format(self.title)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = u"posts"
        ordering = ['-published_date']



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200, verbose_name=u"Autor")
    text = models.TextField(verbose_name=u"Comentario")
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


class DolarPeso(models.Model):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    name = models.CharField(verbose_name=u"Nombre", max_length=250)
    bid = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    ask = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    rate = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.name, self.created_date)

    def __unicode__(self):
        return "{} - {}".format(self.name, self.created_date)

    class Meta:
        verbose_name = "Cambio dolar"
        verbose_name_plural = u"Historial pesos/dolar   "
