from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"post", views.PostCreateView)
router.register(r"tag", views.TagCreateView)

urlpatterns = router.urls
