from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("", include("django_fast.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("robots.txt", include("robots.urls")),
    path("api/", include("snippets.urls")),
    path("eduardo/", admin.site.urls),
]

urlpatterns += i18n_patterns(  # type: ignore
    path("", include("blog.urls")),
)


if settings.DEBUG:
    import debug_toolbar  # type: ignore # noqa

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
        path("rosetta/", include("rosetta.urls")),
    ]
