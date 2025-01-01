# project/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("admin/cache-explorer/", views.cache_explorer, name="cache_explorer"),
    path("admin/cache-explorer/<str:alias>/", views.cache_detail, name="cache_detail"),
]
