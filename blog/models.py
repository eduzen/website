from django.contrib.sitemaps import ping_google
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.urls import reverse

from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from djmoney.models.fields import MoneyField


class Tag(models.Model):
    word = models.CharField(max_length=50)
    slug = models.CharField(max_length=250)

    def __str__(self):
        return self.slug


class PostQuerySet(models.QuerySet):
    def published(self):
        # -- only active records
        return self.filter(published_date__isnull=False).prefetch_related("tags")


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Titulo")
    pompadour = models.CharField(
        max_length=800, null=True, blank=True, verbose_name="Resumen para portada"
    )
    slug = AutoSlugField(
        editable=True,
        null=True,
        blank=True,
        unique=True,
        populate_from="title",
        verbose_name="Url",
    )
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    text = RichTextUploadingField(verbose_name="Cuerpo de texto")
    image = models.ImageField(upload_to="post-img/%Y/%m/%d", blank=True, null=True)

    objects = PostQuerySet.as_manager()

    def image_tag(self):
        img = ""
        if self.image:
            img = "<img src='{}' width='100' height='100'/>".format(self.image.url)
        return mark_safe(img)

    image_tag.short_description = "Image"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def published(self):
        return True if self.published_date else False

    published.boolean = True
    published.short_description = "Published"

    def get_absolute_url(self):
        return reverse("post_slug", args=[self.slug])

    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-published_date"]


class Comment(models.Model):
    post = models.ForeignKey("blog.Post", related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=200, verbose_name="Autor")
    text = models.TextField(verbose_name="Comentario")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class CustomPage(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=250)

    slug = AutoSlugField(populate_from="name")

    include_header = models.BooleanField(default=True, verbose_name="Incluir header")

    include_footer = models.BooleanField(default=True, verbose_name="Incluir footer")

    include_contact_form = models.BooleanField(
        default=True, verbose_name="Incluir formulario de contacto"
    )

    content = RichTextUploadingField(verbose_name="Contenido", null=True, blank=True)

    def get_absolute_url(self):
        return reverse("blog:post", args=(self.slug,))

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Páginas custom"
        verbose_name_plural = "Páginas custom"


@python_2_unicode_compatible
class DolarPeso(models.Model):
    balance = MoneyField(max_digits=10, decimal_places=2)
    name = models.CharField(verbose_name="Nombre", max_length=250)
    bid = MoneyField(max_digits=10, decimal_places=2)
    ask = MoneyField(max_digits=10, decimal_places=2)
    rate = MoneyField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.name, self.created_date)

    class Meta:
        verbose_name = "Cambio dolar"
        verbose_name_plural = "Historial pesos/dolar   "
