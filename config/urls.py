from django.urls import path

from . import views

urlpatterns = [path("", views.Google.as_view(), name="google")]
