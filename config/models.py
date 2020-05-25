from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from solo.models import SingletonModel


class BioConfiguration(SingletonModel):
    title = models.CharField(max_length=255, default="Quién les escribe")
    subtitle = models.CharField(max_length=255, blank=True)
    small = RichTextUploadingField(null=True, blank=True)
    long = RichTextUploadingField(null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    bio_pic = models.ImageField(null=True, upload_to="bio-pic/%Y/%m/%d")
    pic_0 = models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d")
    pic_1 = models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d")
    pic_2 = models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d")

    def __str__(self):
        return "Pagina de Bio/About"

    class Meta:
        verbose_name = "Bio/About configuration"
