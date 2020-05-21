from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    bucket_name = "oak-statics"
    location = settings.STATICFILES_LOCATION
    custom_domain = "oak-statics.s3.amazonaws.com"


class MediaStorage(S3Boto3Storage):
    bucket_name = "oak-demo"
    location = settings.MEDIAFILES_LOCATION
