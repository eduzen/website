# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField
from meta.models import ModelMeta
from ckeditor_uploader.fields import RichTextUploadingField
from djmoney.models.fields import MoneyField

@python_2_unicode_compatible
class Tag(models.Model):
    word = models.CharField(max_length=50)
    slug = models.CharField(max_length=250)

    def __str__(self):
        return self.slug


@python_2_unicode_compatible
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

    @models.permalink
    def get_absolute_url(self):
        return 'blog:post', (self.slug,)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = u"posts"
        ordering = ['-published_date']


@python_2_unicode_compatible
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


@python_2_unicode_compatible
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

    class Meta:
        verbose_name = "Páginas custom"
        verbose_name_plural = u"Páginas custom"


@python_2_unicode_compatible
class DolarPeso(models.Model):
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    name = models.CharField(verbose_name=u"Nombre", max_length=250)
    bid = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    ask = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    rate = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.name, self.created_date)

    class Meta:
        verbose_name = "Cambio dolar"
        verbose_name_plural = u"Historial pesos/dolar   "
