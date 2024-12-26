import logging

from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# from ckeditor_uploader.fields import RichTextUploadingField  # type: ignore
from django_ckeditor_5.fields import (
    CKEditor5Field as RichTextUploadingField,  # type: ignore
)
from image_cropping import ImageRatioField  # type: ignore

logger = logging.getLogger(__name__)


class Tag(models.Model):
    word = models.CharField(unique=True, max_length=50, verbose_name=_("word"))
    slug = models.SlugField(null=False, blank=True, max_length=50, db_index=True, verbose_name=_("slug"))

    class Meta:
        unique_together = (("word", "slug"),)
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.slug or "-"


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_date__isnull=False).prefetch_related("tags")

    def count_tags(self):
        return (
            self.published()
            .only("tags__slug")
            .values("tags__slug")
            .annotate(total=Count("tags__slug"))
            .order_by("-total")
        )


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_("title"))
    summary = models.CharField(max_length=800, blank=True, verbose_name=_("summary"))
    suggestions = models.JSONField(blank=True, null=True)
    slug = models.SlugField(null=True, unique=True, db_index=True, verbose_name=_("slug"))
    created_date = models.DateField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    text = RichTextUploadingField(verbose_name=_("Body text"))

    image = models.ImageField(upload_to="post-img/%Y/%m/%d", blank=True, null=True)
    cropping = ImageRatioField("image", "260x120")  # type: ignore

    objects = PostQuerySet.as_manager()

    def publish(self) -> None:
        self.published_date = timezone.now()
        self.save()

    @property
    def published(self) -> bool:
        return True if self.published_date else False

    def get_absolute_url(self) -> str:
        return reverse("post_detail", args=[self.slug])

    def __str__(self):
        return self.slug or "-"

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-published_date"]
