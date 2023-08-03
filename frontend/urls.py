from django.urls import path

from . import views

urlpatterns = [
    path("", views.BaseView.as_view(), name="home"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("about", views.AboutView.as_view(), name="about"),
    path("blog", views.HomeListView.as_view(), name="blog"),
    path("consultancy", views.ConsultancyView.as_view(), name="consultancy"),
]
