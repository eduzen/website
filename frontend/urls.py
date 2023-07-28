from django.urls import path

from . import views

urlpatterns = [
    path("base", views.BaseView.as_view(), name="base"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("about", views.AboutView.as_view(), name="about"),
]
