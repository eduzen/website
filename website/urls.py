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
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views
from django.views.generic.base import RedirectView

from rest_framework.documentation import include_docs_urls

favicon_view = RedirectView.as_view(url="/static/config/img/favicon.ico", permanent=True)


urlpatterns = [
    url(r"^favicon\.ico$", favicon_view),
    url(r"^eduardo/", admin.site.urls),
    url(r"^ckeditor/", include("ckeditor_uploader.urls")),
    url(r"^robots\.txt", include("robots.urls")),
    url(r"^google448c52311d45450b.html", include("config.urls")),
    url(r"^", include("blog.urls")),
    url(r"^api/", include("api.urls")),
    url(r"^telegram/", include("expenses.urls")),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^docs/", include_docs_urls(title="My eduzen API title")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
