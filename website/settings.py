import os
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from configurations import Configuration, values


class Base(Configuration):
    SITE_ID = 1
    SECRET_KEY = values.SecretValue()
    BASE_DIR = Path(".").resolve(strict=True).parent.parent
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGE_CODE = "es-ar"
    LOG_LEVEL = values.Value("INFO")
    TIME_ZONE = "America/Argentina/Buenos_Aires"

    LOGIN_REDIRECT_URL = "/"
    APPEND_SLASH = True
    DEBUG = False
    SECRET_KEY = values.SecretValue()

    CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
    ANYMAIL = values.Value({})
    DEFAULT_FROM_EMAIL = values.Value()
    DATABASES = values.DatabaseURLValue()

    DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sitemaps",
        "django.contrib.sites",
        "django.contrib.postgres",
    ]

    THIRD_PARTY_APPS = [
        "captcha",
        "anymail",
        "crispy_forms",
        "ckeditor",
        "ckeditor_uploader",
        "solo",
        "robots",
        "djmoney",
        "rest_framework",
        "django_extensions",
    ]

    # Application definition
    APPS = ["config", "blog", "api", "expenses"]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "website.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.i18n",
                ]
            },
        }
    ]

    WSGI_APPLICATION = "website.wsgi.application"

    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/1.10/topics/i18n/

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/

    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"

    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    # STATICFILES_DIRS = [os.path.join(BASE_DIR, "assets")]

    CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min."
    CKEDITOR_UPLOAD_PATH = "/"
    CKEDITOR_CONFIGS = {
        "awesome_ckeditor": {"toolbar": "full"},
        "default": {
            "toolbar": "full",
            "autoParagraph": "false",
            "breakBeforeOpen": "false",
            "breakAfterOpen": "false",
            "breakBeforeClose": "false",
            "breakAfterClose": "false",
            "enterMode": "false",
            "extraPlugins": ",".join(["codesnippet"]),
        },
        "autoParagraph": "false",
    }

    # Crispy Forms
    CRISPY_TEMPLATE_PACK = "bootstrap3"

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
        ),
    }

    CAPTCHA_CHALLENGE_FUNCT = "captcha.helpers.random_char_challenge"
    CAPTCHA_LENGTH = 10
    CAPTCHA_TIMEOUT = 1
    CAPTCHA_LETTER_ROTATION = (-45, 45)
    TEST_RUNNER = "website.runner.PytestTestRunner"

    @property
    def INSTALLED_APPS(self):
        return self.DJANGO_APPS + self.THIRD_PARTY_APPS + self.APPS


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = values.ListValue(["*"])

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "mailhog"  # Your Mailhog Host
    EMAIL_PORT = "1025"

    ANYMAIL = {
        "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN"),
    }

    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None
    INTERNAL_IPS = ["127.0.0.1"]

    @property
    def DEBUG_TOOLBAR_CONFIG(self):
        return {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ["debug_toolbar"]

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # NOQA


class Prod(Base):
    ALLOWED_HOSTS = values.ListValue(["eduzen.com.ar"])
    STATIC_URL = "https://static.eduzen.com.ar/"
    MEDIA_URL = "https://media.eduzen.com.ar/"
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    SERVER_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")
    SENTRY_DSN = values.Value()
    DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
    DROPBOX_OAUTH2_TOKEN = values.SecretValue()
    DROPBOX_ROOT_PATH = values.Value()
    DROPBOX_TIMEOUT = values.IntegerValue()

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

    @classmethod
    def post_setup(cls):
        """Sentry initialization"""
        super().post_setup()
        sentry_sdk.init(dsn=cls.SENTRY_DSN, integrations=[DjangoIntegration()])


class Test(Base):
    SECRET_KEY = "sometestingkey"
    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
