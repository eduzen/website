from rest_framework import viewsets

from api.serializers import PostSerializer
from blog.models import Post


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.prefetch_related("tags").published()
    serializer_class = PostSerializer
