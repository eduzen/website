import os

from configurations import values

from .base import Base, DropboxStorage, Sentry, WhitenoiseStatic


class Dokku(DropboxStorage, Sentry, WhitenoiseStatic, Base):
    DEBUG = False

    DATABASES = values.DatabaseURLValue(conn_max_age=600, ssl_require=False)
    REDIS_URL = values.Value(environ_name="REDIS_URL")

    # Cache key TTL in seconds
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    CACHE_MIDDLEWARE_SECONDS = DAY

    @property
    def CACHES(self):
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": os.environ.get("REDIS_URL"),
                "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            }
        }

    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    SERVER_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")
    MAILGUN_API_KEY = values.Value()
    MAILGUN_SENDER_DOMAIN = values.Value()

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
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
                "aws": {
                    # you can add specific format for aws here
                    # if you want to change format, you can read:
                    #    https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
                    "format": "%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
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

    """
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "aws": {
                # you can add specific format for aws here
                # if you want to change format, you can read:
                #    https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
                "format": "%(asctime)s [%(levelname)-8s] %(message)s [%(pathname)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "aws"}},
        "loggers": {
            "*": {"handlers": ["console", "watchtower"], "level": "ERROR", "propagate": True},
            "django": {"handlers": ["console", "watchtower"], "propagate": False, "level": "ERROR"},
        },
    }
    """

    ALLOWED_HOSTS = [
        ".eduzen.com.ar",
        ".eduardoenriquez.com.ar",
        ".eduzen.ar",
        "167.99.230.241",
    ]
