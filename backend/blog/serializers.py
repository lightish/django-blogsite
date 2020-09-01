from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import BlogPost


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'avatar')


class BlogPostShortSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'category', 'thumbnail',
                  'created_on', 'author')
        read_only_fields = ('id', 'created_on', 'author')


class BlogPostLongSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'category', 'thumbnail',
                  'created_on', 'author')
        read_only_fields = ('id', 'created_on', 'author')
