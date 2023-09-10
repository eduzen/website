from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from .sitemap import sitemaps
from .views import MediaView, favicon_view

urlpatterns = [
    path("", include("core.urls")),
    path("healthchecks/", include("django_healthchecks.urls")),
    path("media/<path>", MediaView.as_view()),
    path("favicon.ico", favicon_view),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("robots.txt", include("robots.urls")),
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemaps"),
]

urlpatterns += i18n_patterns(
    path("", include("blog.urls")),
    path("eduardo/", admin.site.urls),
)


if settings.DEBUG:
    import debug_toolbar  # type: ignore # noqa

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
        path("rosetta/", include("rosetta.urls")),
    ] + urlpatterns
