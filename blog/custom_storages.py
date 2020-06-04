from storages.backends.s3boto3 import S3Boto3Storage


class MediaPublicStorage(S3Boto3Storage):
    bucket_name = "eduzen-public-media"
    custom_domain = "eduzen-public-media.s3.amazonaws.com"
