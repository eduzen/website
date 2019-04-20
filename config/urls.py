from django.conf.urls import url
from . import views

urlpatterns = [url(r"^$", views.Google.as_view(), name="google")]
