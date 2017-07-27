from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^posts/$', views.PostCreateView.as_view(), name="post_create"),
    url(r'^tags/$', views.TagCreateView.as_view(), name="tag_create"),
]
