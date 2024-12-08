from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"snippets", views.SnippetModelViewSet)

urlpatterns = router.urls

urlpatterns = [
    # Include the API routes
    path("api/", include(router.urls)),
]
