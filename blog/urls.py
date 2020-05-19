# from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path

from . import views
from .sitemap import sitemaps

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("post/", views.PostListView.as_view(), name="post_list"),
    path("blog/", views.PostListView.as_view(), name="blog"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("bio/", views.AboutView.as_view(), name="about"),
    path("clases/", views.ClasesView.as_view(), name="clases"),
    path("tags/<str:tag>/", views.PostTagsList.as_view(), name="bytag"),
    path("search/", views.AdvanceSearch.as_view(), name="search"),
    path("buscar/", views.AdvanceSearch.as_view(), name="search"),
    path("contactar/", views.ContactView.as_view(), name="contact"),
    path("contacto/", views.ContactView.as_view(), name="contact"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("blog/<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
    path("blog/<slug:slug>/", views.PostDetail.as_view(), name="post_slug"),
    path("sucess/", views.SucessView.as_view(), name="sucess"),
    path("error/", views.ErrorView.as_view(), name="error"),
    # Example: /2012/aug/
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$", views.PostMonthArchiveView.as_view(), name="archive_month"),
    # Example: /2012/08/
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$",
        views.PostMonthArchiveView.as_view(month_format="%m"),
        name="archive_month_numeric",
    ),
    # Example: /2012/week/23/
    re_path(r"^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$", views.PostWeekArchiveView.as_view(), name="archive_week"),
    # Example: /2012/nov/10/
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$",
        views.PostDayArchiveView.as_view(),
        name="archive_day",
    ),
    path("archive/", views.PostArchiveIndex.as_view(), name="post_archive"),
    re_path(r"^sitemap-(?P<section>.+)\.xml$", sitemap, {"sitemaps": sitemaps}),
    re_path(r"^sitemap\.xml$", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemaps"),
]
