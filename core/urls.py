from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import RedirectView

from . import views
from .sitemap import sitemaps

urlpatterns = [
    path("", RedirectView.as_view(url="/en/", permanent=True), name="root_redirect"),
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemaps"),
    path("media/<path>", views.MediaView.as_view()),
    path("favicon.ico", views.favicon_view),
    path("version/", views.version_view, name="version"),
    path("language-dropdown/", views.language_dropdown, name="language_dropdown"),
    path("chatgpt_improve_post/<int:post_id>/", views.chatgpt_improve_post, name="chatgpt_improve_post"),
]
