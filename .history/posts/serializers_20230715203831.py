from rest_framework import serializers
from .models import Post, PostImage, CustomFieldValue
from users.models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'avatar')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'is_featured')


class CustomFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldValue
        fields = ('id', 'field', 'value')


class PostSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer()
    images = PostImageSerializer(many=True, read_only=True)
    custom_fields = CustomFieldValueSerializer(many=True, read_only=True)
    published_at = serializers.DateTimeField(format="%m-%d-%Y")
    class Meta:
        model = Post
        fields = ('id', 'author', 'post_type', 'title', 'slug', 'content', 'published_at',
                  'categories', 'tags', 'custom_fields', 'readtime', 'likes', 'dislikes', 'images')
