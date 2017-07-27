from rest_framework import generics
from .serializers import PostSerializer
from .serializers import TagSerializer
from blog.models import Post
from blog.models import Tag


class PostCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class TagCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
