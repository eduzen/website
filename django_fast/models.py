from datetime import timedelta

from django.db import models
from django.utils import timezone


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

    class Meta:
        indexes = [
            models.Index(fields=["-start_time"], name="reqprofile_start_time_idx"),
            models.Index(fields=["path"], name="reqprofile_path_idx"),
            models.Index(fields=["status_code"], name="reqprofile_status_idx"),
            models.Index(fields=["-start_time", "path"], name="reqprofile_time_path_idx"),
        ]

    def __str__(self):
        return f"{self.method} {self.path} - {self.duration_ms} ms"

    @classmethod
    def cleanup_old_records(cls, days: int = 30) -> int:
        """Delete records older than specified days. Returns count of deleted records."""
        cutoff = timezone.now() - timedelta(days=days)
        deleted, _ = cls.objects.filter(start_time__lt=cutoff).delete()
        return deleted
