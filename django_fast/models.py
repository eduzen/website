from django.db import models


class CacheExplorer(models.Model):
    class Meta:
        app_label = "django_fast"
        verbose_name = "Cache Management"
        verbose_name_plural = "Cache Management"
