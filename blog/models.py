import logging

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sitemaps import ping_google
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from image_cropping import ImageRatioField

logger = logging.getLogger(__name__)


class Tag(models.Model):
    word = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(null=True, max_length=50)

    class Meta:
        unique_together = (("word", "slug"),)

    def __str__(self):
        return self.slug or "-"


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_date__isnull=False).prefetch_related("tags")

    def count_tags(self):
        return self.published().values("tags__slug").annotate(total=Count("tags__slug")).order_by("-total")


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Titulo")
    pompadour = models.CharField(max_length=800, blank=True, verbose_name="Resumen para portada")
    slug = models.SlugField(null=True, unique=True)
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    text = RichTextUploadingField(verbose_name="Cuerpo de texto")

    image = models.ImageField(upload_to="post-img/%Y/%m/%d", blank=True, null=True)
    images = models.ManyToManyField("files.PublicImage", related_name="post")
    snippets = models.ManyToManyField("snippets.Snippet", related_name="post")
    cropping = ImageRatioField("image", "260x120")

    objects = PostQuerySet.as_manager()

    def image_tag(self):
        if not self.image:
            return "Nothing"
        img = f"<img src='{self.image.url}' width='100' height='100'/>"
        return mark_safe(img)

    image_tag.short_description = "Image"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def published(self):
        return True if self.published_date else False

    published.boolean = True

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    def notify_google(self):
        try:
            ping_google()
        except Exception:
            logger.warn("Error trying to inform google")

    def save(self, *args, **kwargs):
        if self.published_date:
            ping_google()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug or "-"

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-published_date"]
