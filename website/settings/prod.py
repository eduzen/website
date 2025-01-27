import logfire
import sentry_sdk
from decouple import Csv, config
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import LOG_LEVEL  # noqa

logfire.configure()
logfire.instrument_django()
logfire.instrument_psycopg()

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=".eduzen.com.ar,.eduardoenriquez.com.ar,.eduzen.ar", cast=Csv())

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600 * 2  # This sets it for 2 hour, adjust the value accordingly.
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False)


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

SENTRY_DSN = config("SENTRY_DSN", default="")
RELEASE = config("SENTRY_RELEASE", default="0.0.0+dev")

if (not DEBUG) and SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,  # type: ignore
        release=RELEASE,  # type: ignore
        enable_tracing=True,
        traces_sample_rate=0.20,
        profiles_sample_rate=0.20,
        integrations=[
            DjangoIntegration(
                cache_spans=True,
                transaction_style="url",
                middleware_spans=True,
                signals_spans=True,
            )
        ],
    )
