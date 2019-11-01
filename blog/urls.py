# from django.urls import path
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemap import sitemaps


urlpatterns = [
    url(r"^$", views.HomeListView.as_view(), name="home"),
    url(r"post", views.PostListView.as_view(), name="post_list"),
    url(r"^blog/$", views.PostListView.as_view(), name="blog"),
    url(r"^about/$", views.AboutView.as_view(), name="about"),
    url(r"^bio/$", views.AboutView.as_view(), name="about"),
    url(r"^clases/$", views.ClasesView.as_view(), name="clases"),
    url(r"^tags/(?P<tag>[\w-]+)/$", views.PostTagsList.as_view(), name="bytag"),
    url(r"^stuff/$", views.stuff, name="stuff"),
    url(r"^util/$", views.stuff, name="stuff"),
    url(r"^search/$", views.advance_search, name="search"),
    url(r"^buscar/$", views.advance_search, name="search"),
    url(r"^contactar/$", views.ContactView.as_view(), name="contact"),
    url(r"^contacto/$", views.ContactView.as_view(), name="contact"),
    url(r"^contact/$", views.ContactView.as_view(), name="contact"),
    url(r"^custom/(?P<slug>[\w-]+)/$", views.custom_page, name="custom_page"),
    url(r"^blog/(?P<pk>[0-9]+)/$", views.post_detail, name="post_detail"),
    url(r"^blog/(?P<slug>[\w-]+)/$", views.post_slug, name="post_slug"),
    # Example: /2012/aug/
    url(
        r"^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$",
        views.PostMonthArchiveView.as_view(),
        name="archive_month",
    ),
    # Example: /2012/08/
    url(
        r"^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$",
        views.PostMonthArchiveView.as_view(month_format="%m"),
        name="archive_month_numeric",
    ),
    # Example: /2012/week/23/
    url(
        r"^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$",
        views.PostWeekArchiveView.as_view(),
        name="archive_week",
    ),
    # Example: /2012/nov/10/
    url(
        r"^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$",
        views.PostDayArchiveView.as_view(),
        name="archive_day",
    ),
    url(r"^archive/$", views.PostArchiveIndex.as_view(), name="post_archive"),
    url(r"^sitemap-(?P<section>.+)\.xml$", sitemap, {"sitemaps": sitemaps}),
    url(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemaps",
    ),
]
