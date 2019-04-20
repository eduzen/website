from django.conf.urls import url

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    url(r"^posts/$", views.PostCreateView.as_view(), name="post_create"),
    url(r"^tags/$", views.TagCreateView.as_view(), name="tag_create"),
]

urlpatterns += router.urls
