from django.db import models


class CacheExplorer(models.Model):
    class Meta:
        app_label = "django_fast"
        verbose_name = "Cache Management"
        verbose_name_plural = "Cache Management"


class RequestProfile(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    status_code = models.PositiveIntegerField()
    user = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_ms = models.FloatField()

    def __str__(self):
        return f"{self.method} {self.path} - {self.duration_ms} ms"
