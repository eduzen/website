import os

from configurations import values

from .base import Base, DropboxStorage, Sentry, WhitenoiseStatic


class Prod(DropboxStorage, Sentry, WhitenoiseStatic, Base):
    DEBUG = True

    SECRET_KEY = values.Value()
    ALLOWED_HOSTS = values.ListValue(["eduzen.com.ar"])
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    SERVER_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")

    MAILGUN_API_KEY = values.Value()
    MAILGUN_SENDER_DOMAIN = values.Value()

    # Cache key TTL in seconds
    MINUTE = 60

    HOUR = MINUTE * 60
    DAY = HOUR * 24
    CACHE_MIDDLEWARE_SECONDS = DAY
    DATABASES = values.DatabaseURLValue(conn_max_age=600, ssl_require=False)

    CACHE = values.CacheURLValue()

    @property
    def CACHES(self):
        self.CACHE["default"]["OPTIONS"] = {"CLIENT_CLASS": "django_redis.client.DefaultClient"}
        return self.CACHE

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
