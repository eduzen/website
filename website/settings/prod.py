from .base import *  # noqa
from .base import LOG_LEVEL  # noqa
import sentry_sdk
from decouple import config, Csv

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=".eduzen.com.ar,.eduardoenriquez.com.ar,.eduzen.ar", cast=Csv())

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://*.eduzen.ar,https://*.eduzen.com.ar,https://*.eduardoenriquez.com.ar",
    cast=Csv(),
)

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.eduzen\.ar$",
    r"^https://localhost$",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": ("[DJANGO] %(levelname)s %(asctime)s %(module)s " "%(name)s.%(funcName)s:%(lineno)s: %(message)s")
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {"console": {"level": LOG_LEVEL, "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "*": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": True},
        "django": {"handlers": ["console"], "propagate": False, "level": LOG_LEVEL},
    },
}

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
# GS_BUCKET_NAME = config('GS_BUCKET_NAME')
# GS_PROJECT_ID = config('GS_PROJECT_ID')

SENTRY_DSN = config("SENTRY_DSN", default="")
RELEASE = config("SENTRY_RELEASE", default="0.0.0+dev")

if (not DEBUG) and SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,  # type: ignore
        release=RELEASE,  # type: ignore
        traces_sample_rate=0.10,
        profiles_sample_rate=0.10,
    )
