import os

from configurations import values

from .base import BASE_DIR, Base, Sentry, WhitenoiseStatic


class Prod(Sentry, WhitenoiseStatic, Base):
    DEBUG = False
    ALLOWED_HOSTS = values.ListValue(["eduzen.com.ar"])

    MEDIA_URL = "https://media.eduzen.ar/"
    MEDIA_ROOT = BASE_DIR / "media"

    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    SERVER_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")

    MAILGUN_API_KEY = values.Value()
    MAILGUN_SENDER_DOMAIN = values.Value()

    # Cache key TTL in seconds
    MINUTE = 60

    HOUR = MINUTE * 60
    DAY = HOUR * 24
    CACHE_MIDDLEWARE_SECONDS = HOUR
    DATABASES = values.DatabaseURLValue()

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        # "website.middleware.CloudflareMiddleware",
    ]

    @property
    def ANYMAIL(self):
        return {
            "MAILGUN_API_KEY": self.MAILGUN_API_KEY,
            "MAILGUN_SENDER_DOMAIN": self.MAILGUN_SENDER_DOMAIN,
        }

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ["storages"]

    @property
    def LOGGING(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": (
                        "[DJANGO] %(levelname)s %(asctime)s %(module)s " "%(name)s.%(funcName)s:%(lineno)s: %(message)s"
                    )
                },
                "verbose": {
                    "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                    "datefmt": "%d/%b/%Y %H:%M:%S",
                },
                "simple": {"format": "%(levelname)s %(message)s"},
            },
            "handlers": {
                "console": {"level": self.LOG_LEVEL, "class": "logging.StreamHandler", "formatter": "verbose"}
            },
            "loggers": {
                "*": {"handlers": ["console"], "level": self.LOG_LEVEL, "propagate": True},
                "django": {"handlers": ["console"], "propagate": False, "level": self.LOG_LEVEL},
            },
        }
