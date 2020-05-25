from django.db import models

from image_cropping import ImageRatioField


class PublicImage(models.Model):
    title = models.CharField(max_length=200, blank=True, default="")
    image = models.FileField(upload_to="public/images/%Y/%m/")

    cropping = ImageRatioField("image", "260x120")

    def __str__(self):
        return self.title
