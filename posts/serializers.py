from rest_framework import serializers
from .models import Post, PostImage, CustomFieldValue, Tag, Category,PostType
from users.models import UserAccount

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategoryValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    categories = CategoryValueSerializer(many=True, read_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True, required=False)
    published = serializers.DateTimeField(format="%m-%d-%Y", required=False)
    updated = serializers.DateTimeField(format="%m-%d-%Y", required=False)
    post_type = PostTypeSerializer( required=False )
    lookup_field = 'slug'
    pagination_class = []
    class Meta:
        model = Post
        fields = ( 'title', 'slug', 'content', 'post_type','published','updated',
                  'categories', 'tags', 'readtime', 'likes', 'dislikes', 'featured_image', 'post_image_1', 'post_image_2', 'post_image_3')
        
    def get_post_type(self, obj):
        return obj.post_type.name if obj.post_type else None
    
class RecentPostSerializer(serializers.ModelSerializer):
    categories = CategoryValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    published = serializers.DateTimeField(format="%m-%d-%Y")
    updated = serializers.DateTimeField(format="%m-%d-%Y")
    post_type = PostTypeSerializer()

    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'published', 'updated', 'post_type',
                  'categories', 'tags', 'readtime', 'likes', 'dislikes', 'featured_image', 'post_image_1', 'post_image_2', 'post_image_3')
