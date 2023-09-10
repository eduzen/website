from django.urls import path
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemap import sitemaps

urlpatterns = [
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemaps"),
    path("media/<path>", views.MediaView.as_view()),
    path("favicon.ico", views.favicon_view),
    path("language-dropdown/", views.language_dropdown, name="language_dropdown"),
    path("chatgpt_improve_post/<int:post_id>/", views.chatgpt_improve_post, name="chatgpt_improve_post"),
]
