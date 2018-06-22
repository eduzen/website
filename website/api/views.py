from django.contrib.auth.models import User, Group

from rest_framework import generics
from rest_framework import viewsets

from .serializers import PostSerializer
from .serializers import TagSerializer
from .serializers import UserSerializer
from .serializers import GroupSerializer

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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = (permissions.IsAuthenticated,)
