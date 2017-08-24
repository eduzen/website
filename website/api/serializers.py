""" Serializers for api app """
from django.contrib.auth.models import User, Group

from rest_framework import serializers

from blog.models import Post
from blog.models import Tag


class PostSerializer(serializers.ModelSerializer):
    """Serializer to map the Post instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Post
        fields = ('author', 'title', 'pompadour',  'tags', 'text',
                  'slug', 'created_date', 'published_date',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer to map the Tag instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Tag
        fields = ('word', 'slug',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the user instance into JSON format."""

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
