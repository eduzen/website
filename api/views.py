from django.contrib.auth.models import Group, User
from rest_framework import viewsets

from blog.models import Post, Tag

from .serializers import GroupSerializer, PostSerializer, TagSerializer, UserSerializer


class PostCreateView(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TagCreateView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
