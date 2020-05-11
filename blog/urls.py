# from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path

from . import views
from .sitemap import sitemaps

urlpatterns = [
    re_path(r"^$", views.HomeListView.as_view(), name="home"),
    path("post/", views.PostListView.as_view(), name="post_list"),
    re_path(r"^blog/$", views.PostListView.as_view(), name="blog"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("bio/", views.AboutView.as_view(), name="about"),
    re_path(r"^clases/$", views.ClasesView.as_view(), name="clases"),
    re_path(r"^tags/(?P<tag>[\w-]+)/$", views.PostTagsList.as_view(), name="bytag"),
    path("stuff/", views.StuffView.as_view(), name="stuff"),
    path("util/", views.StuffView.as_view(), name="stuff"),
    path("search/", views.AdvanceSearch.as_view(), name="search"),
    path("buscar/", views.AdvanceSearch.as_view(), name="search"),
    path("contactar/", views.ContactView.as_view(), name="contact"),
    path("contacto/", views.ContactView.as_view(), name="contact"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    re_path(r"^custom/(?P<slug>[\w-]+)/$", views.custom_page, name="custom_page"),
    re_path(r"^blog/(?P<pk>[0-9]+)/$", views.post_detail, name="post_detail"),
    re_path(r"^blog/(?P<slug>[\w-]+)/$", views.post_slug, name="post_slug"),
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
