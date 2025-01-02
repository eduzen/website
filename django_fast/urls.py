# django_fast/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("admin/cache-explorer/", views.CacheExplorerView.as_view(), name="cache_explorer"),
    path("admin/cache-explorer/<str:alias>/", views.CacheDetailView.as_view(), name="cache_detail"),
    path("admin/cache-explorer/<str:alias>/clear/", views.CacheDetailView.as_view(), name="cache_clear"),
    path("admin/cache-explorer/<str:alias>/ping/", views.CacheDetailView.as_view(), name="cache_ping"),
]
