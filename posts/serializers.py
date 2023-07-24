from rest_framework import serializers
from .models import Post, PostImage, CustomFieldValue, Tag, Category
from users.models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'avatar')

class PostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ('id', 'image', 'is_featured', 'image_url')

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

class CustomFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldValue
        fields = ('id', 'field', 'value')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug')


class CategoryValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')



class PostSerializer(serializers.ModelSerializer):
    # author = UserAccountSerializer()
    # custom_fields = CustomFieldValueSerializer(many=True, read_only=True)
    categories = CategoryValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    published_at = serializers.DateTimeField(format="%m-%d-%Y")

    class Meta:
        model = Post
        fields = ( 'title', 'slug', 'content', 'published_at', 'post_type',
                  'categories', 'tags', 'readtime', 'likes', 'dislikes', 'featured_image', 'post_image_1', 'post_image_2', 'post_image_3')

class RecentPostSerializer(serializers.ModelSerializer):
    categories = CategoryValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    published_at = serializers.DateTimeField(format="%m-%d-%Y")

    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'published_at', 'post_type',
                  'categories', 'tags', 'readtime', 'likes', 'dislikes', 'featured_image', 'post_image_1', 'post_image_2', 'post_image_3')
