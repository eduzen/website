from rest_framework import serializers
from blog.models import Post
from blog.models import Tag


class PostSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Post
        fields = ('author', 'title', 'pompadour',  'tags', 'text',
                  'slug', 'created_date', 'published_date',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Tag
        fields = ('word', 'slug',)
