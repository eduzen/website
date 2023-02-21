from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from rest_framework.authtoken import views

from .sitemap import sitemaps
from .views import MediaView, favicon_view

urlpatterns = [
    path("healthchecks/", include("django_healthchecks.urls")),
    path("", include("snippets.urls")),
    path("media/<path>", MediaView.as_view()),
    path("favicon.ico", favicon_view),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("robots.txt", include("robots.urls")),
    path("google448c52311d45450b.html", include("config.urls")),
    path("telegram/", include("expenses.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("captcha/", include("captcha.urls")),
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemaps"),
    path("api-token-auth/", views.obtain_auth_token, name="api-token-auth"),
]

urlpatterns += i18n_patterns(
    path("", include("blog.urls")),
    path("eduardo/", admin.site.urls),
)


if settings.DEBUG:
    import debug_toolbar  # NOQA

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns  # NOQA
