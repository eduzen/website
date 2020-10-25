"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from .views import MediaView, favicon_view

urlpatterns = [
    path("api/", include("snippets.urls")),
    path("media/<path>", MediaView.as_view()),
    path("favicon.ico", favicon_view),
    path("eduardo/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("robots.txt", include("robots.urls")),
    path("google448c52311d45450b.html", include("config.urls")),
    path("telegram/", include("expenses.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("captcha/", include("captcha.urls")),
    path("", include("blog.urls")),
]

urlpatterns += i18n_patterns(
    path(
        "",
        include("blog.urls"),
    )
)


if settings.DEBUG:
    import debug_toolbar  # NOQA

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns  # NOQA
