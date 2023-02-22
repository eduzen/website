from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ["url", "title", "text", "published_date", "author", "tags"]
