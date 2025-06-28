import re
from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as db_url
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.conf import Settings as thumbnail_settings  # type: ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-)b*6^n!osj#+4-*5aag6d106&@haowpc9_c0**nvw-sg#e-c9h")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1", cast=Csv())

# Application definition
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
    "rest_framework",
    "ckeditor",
    "ckeditor_uploader",
    "corsheaders",
    "crispy_forms",
    "crispy_tailwind",
    "django_extensions",
    "django_htmx",
    "template_partials",
    "easy_thumbnails",
    "image_cropping",
    "robots",
    "rosetta",
]

APPS = [
    "django_fast",
    "blog",
    "snippets",
    "core",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.CloudflareRealIPMiddleware",
    "django_fast.middleware.ProfilerMiddleware",
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
                "core.context_processor.global_data",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"

# Database
DATABASES: dict = {
    'default': config(
        'DATABASE_URL',
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        cast=db_url
    )
}

DATABASES['default'].setdefault("OPTIONS", {}).update({"pool": True})  # NOQA


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Español")),
]

LOCALE_PATHS = (BASE_DIR / "website/locale",)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# # Media files
# MEDIA_URL = config("MEDIA_URL", default="https://media.eduzen.ar/")
# MEDIA_ROOT = config("MEDIA_PATH", default=BASE_DIR / "media")

# GCP settings
GS_BUCKET_NAME = config("GS_BUCKET_NAME", default="media-eduzen-website")
GS_PROJECT_ID = config("GS_PROJECT_ID", default="eduzen-website")
GS_IS_GZIPPED = True
GS_DEFAULT_ACL = "publicRead"  # Make the files public

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_JQUERY_URL = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"
CKEDITOR_UPLOAD_PATH = "/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "basic",
        "width": "100%",
    },
}

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", default="foo")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID", default="foo")

LOG_LEVEL = config("LOG_LEVEL", default="INFO")

LOGIN_REDIRECT_URL = "/"
APPEND_SLASH = True

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 8,
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# Django Image Cropping: https://github.com/jonasundderwolf/django-image-cropping
THUMBNAIL_PROCESSORS = ("image_cropping.thumbnail_processors.crop_corners",) + thumbnail_settings.THUMBNAIL_PROCESSORS

# Crispy Forms: https://github.com/django-crispy-forms/crispy-tailwind
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# ChatGPT:
OPENAI_ORGANIZATION = config("OPENAI_ORGANIZATION", default="")
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_MODEL = config("OPENAI_MODEL", default="openai:gpt-4o")
PYDANTIC_AI_MODEL = OPENAI_MODEL

IGNORABLE_404_URLS = [
    re.compile(r"\.php$"),
    re.compile(r"^/wp-"),
]

BUILD_DATE = config("BUILD_DATE", default="unknown")
RELEASE = config("RELEASE", default="unknown")
