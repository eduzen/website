from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemap import sitemaps

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("search/", views.AdvanceSearch.as_view(), name="search"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("post/", views.PostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("blog/", views.PostListView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.PostDetail.as_view(), name="blog_slug"),
    path("tags/<str:tag>/", views.PostTagsList.as_view(), name="bytag"),
    path("sucess/", views.SucessView.as_view(), name="sucess"),
    path("error/", views.ErrorView.as_view(), name="error"),
    path("sitemap-<section>.xml", sitemap, {"sitemaps": sitemaps}),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemaps"),
    path("config", views.Google.as_view(), name="google"),
]
