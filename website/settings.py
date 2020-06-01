import os
from pathlib import Path

import sentry_sdk
from configurations import Configuration, values
from easy_thumbnails.conf import Settings as thumbnail_settings
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(".").resolve(strict=True)


class ConstanceConfig:
    CONSTANCE_DATABASE_CACHE_BACKEND = "default"
    CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

    CONSTANCE_ADDITIONAL_FIELDS = {
        "image_field": ["django.forms.ImageField", {}],
        "url_field": ["django.forms.URLField", {}],
        "email_field": ["django.forms.EmailField", {}],
        "richtext_field": ["django.forms.CharField", {"widget": "ckeditor.widgets.CKEditorWidget"}],
    }

    small = (
        '<p>Hello World! My name is <span style="color: #2980b9">Eduardo</span> '
        'and I&#39;m a <span style="color:#16a085">developer </span>💻. I&#39;ve been working with '
        '<a href="http://www.python.org">Python</a>&nbsp;🐍 for the last 7 years, most of the time working '
        'as a backend developer with <a href="https://www.djangoproject.com/"><span style="color:#16a085">'
        "Django.</span></a></p>"
    )
    longs = """
        <p style="text-align:justify">Hello World! My name is <span style="color:#2980b9">Eduardo</span> and I&#39;m a
        <span style="color:#16a085">developer </span>💻. I&#39;ve been working with
        <a href="http://www.python.org">Python</a>&nbsp;🐍 for the last 7 years, most of the time working as a backend
        developer with <a href="https://www.djangoproject.com/"><span style="color:#16a085">Django</span></a> but I
        also have some experience with <span style="color:#3498db">Flask</span>. I have some experience with Linux 🐧,
        Docker 🐳, Redis <a href="https://emojipedia.org/large-red-square/">🟥</a>,
        <a href="https://www.rabbitmq.com/">RabbitMQ</a> <a href="https://emojipedia.org/rabbit-face/">🐰</a>, and
        <a href="https://docs.celeryproject.org/en/latest/index.html">Celery</a> 🌿.</p>
        <p style="text-align:justify">&nbsp;I develop a telegram bot 🤖:
        <a href="https://github.com/eduzen/bot">https://github.com/eduzen/bot</a>.
        You can talk to him following this link: <a href="https://t.me/eduzen_bot">https://t.me/eduzen_bot</a>.</p>
        <p style="text-align:justify">Besides computers, I like good music, books, philosophy and lately
        <span style="color:#e74c3c">m</span><span style="color:#9b59b6">e</span><span style="color:#e67e22">c
        </span><span style="color:#2ecc71">h</span><span style="color:#f1c40f">a</span><span style="color:#4e5f70">n
        </span><span style="color:#1abc9c">i</span><span style="color:#e74c3c">c</span><span style="color:#f39c12">a
        </span><span style="color:#16a085">l</span> keyboards (right now using a <span style="color:#2980b9">Leo
        </span><span style="color:#7f8c8d">pold</span> <span style="color:#3498db">75</span>
        <span style="color:#7f8c8d">%</span>)! I have a bachelor&#39;s degree in
        <a href="https://en.wikipedia.org/wiki/Philosophy">philosophy</a> from the <a href="http://uba.ar">
        University of Buenos Aires</a>. If you want to see an old picture of me,
        there I go, chatting with Plato 🙄:</p>
    """

    CONSTANCE_CONFIG = {
        "site_name": ("eduzen", "eduzen", str),
        "tab_title": ("eduzen", "eduzen", str),
        "github": ("https://github.com/eduzen", "https://github.com/eduzen", "url_field"),
        "twitter": ("https://twitter.com/_eduzen_", "https://twitter.com/_eduzen_", "url_field"),
        "instagram": ("https://www.instagram.com/eduzen_/", "https://www.instagram.com/eduzen_/", "url_field"),
        "linkedin": (
            "https://linkedin.com/in/enriquezeduardo/",
            "https://linkedin.com/in/enriquezeduardo/",
            "url_field",
        ),
        "email": ("eduardoaenriquez+eduzen@gmail.com", "eduardoaenriquez+eduzen@gmail.com", "email_field"),
        "contact_title": ("Contacto", "Contacto", str),
        "contact_subtitle": ("me arroba eduzen.com.ar", "me arroba eduzen.com.ar", str),
        "contact_body": ("0", "0", "richtext_field"),
        "bio_pic": ("bio_pic.jpg", "", "image_field"),
        "pic_0": ("pic_0.jpg", "", "image_field"),
        "pic_1": ("pic_1.jpg", "", "image_field"),
        "title": ("Eduardo Enriquez", "Eduardo Enriquez", str),
        "subtitle": (
            "Software Engineer in <s>Buenos Aires</s> München",
            "Software Engineer in <s>Buenos Aires</s> München",
            "richtext_field",
        ),
        "small": (small, "", "richtext_field"),
        "long": (longs, "", "richtext_field"),
    }

    CONSTANCE_CONFIG_FIELDSETS = {
        "General Options": ("site_name", "tab_title", "github", "linkedin", "instagram", "twitter", "email"),
        "Contact": ("contact_title", "contact_subtitle", "contact_body"),
        "About me": ("title", "subtitle", "small", "long", "bio_pic", "pic_0", "pic_1", "pic_2",),
    }


class DropboxStorage:
    DROPBOX_OAUTH2_TOKEN = values.SecretValue()
    DROPBOX_ROOT_PATH = values.Value()
    DROPBOX_TIMEOUT = values.IntegerValue()
    DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
    MEDIA_URL = None
    MEDIA_ROOT = None


class WhitenoiseStatic:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "website/static")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


class SelfHostedStorage:
    MEDIA_URL = "https://media.eduzen.com.ar/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


class StaticMedia:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    STATIC_ROOT = os.path.join(BASE_DIR, "website/static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "website/media")


class Sentry:
    SENTRY_DSN = values.Value()

    @classmethod
    def post_setup(cls):
        """Sentry initialization"""
        super().post_setup()  # NOQA
        sentry_sdk.init(dsn=cls.SENTRY_DSN, integrations=[DjangoIntegration()])


class Base(ConstanceConfig, StaticMedia, Configuration):
    SITE_ID = 1
    SECRET_KEY = values.SecretValue()
    BASE_DIR = BASE_DIR
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

    ANYMAIL = values.Value({})
    DEFAULT_FROM_EMAIL = values.Value()
    DATABASES = values.DatabaseURLValue(conn_max_age=600, ssl_require=True)

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
        "easy_thumbnails",
        "image_cropping",
        "constance",
        "constance.backends.database",
    ]

    # Application definition
    APPS = [
        "config",
        "blog",
        "expenses",
        "snippets",
        "files",
    ]

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

    CKEDITOR_JQUERY_URL = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"
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

    THUMBNAIL_PROCESSORS = (
        "image_cropping.thumbnail_processors.crop_corners",
    ) + thumbnail_settings.THUMBNAIL_PROCESSORS

    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

    # Cache key TTL in seconds
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    CACHE_MIDDLEWARE_SECONDS = DAY

    @property
    def CACHES(self):
        self.CACHE["default"]["OPTIONS"] = {"CLIENT_CLASS": "django_redis.client.DefaultClient"}
        return self.CACHE

    @property
    def INSTALLED_APPS(self):
        return self.DJANGO_APPS + self.APPS + self.THIRD_PARTY_APPS


class Dev(Base):
    DEBUG = True
    SECRET_KEY = "s0m3r4nd0mk3yford3v!"
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

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

    @property
    def DEBUG_TOOLBAR_CONFIG(self):
        return {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ["debug_toolbar"]

    @property
    def MIDDLEWARE(self):
        return ["debug_toolbar.middleware.DebugToolbarMiddleware"] + super().MIDDLEWARE


class LocalDev(Dev):
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}


class Test(Dev):
    DEBUG = True
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]

    @property
    def DEBUG_TOOLBAR_CONFIG(self):
        return {
            "SHOW_TOOLBAR_CALLBACK": lambda r: (
                r.environ.get("SERVER_NAME", None) != "testserver"
                and (r.META.get("REMOTE_ADDR", None) in self.INTERNAL_IPS)  # NOQA
            )
        }


class Prod(DropboxStorage, Sentry, WhitenoiseStatic, Base):
    DEBUG = False
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
