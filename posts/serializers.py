from rest_framework import serializers
from .models import Post, Tag, Category,PostType, PostStatus
from django.core.files.base import ContentFile
import base64


class TagSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = Tag
        fields = '__all__'


class CategoryValueSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = Category
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = PostType
        fields = '__all__'

class PostStatusSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = PostStatus
        fields = '__all__'
        
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
    
class PostSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%m-%d-%Y", required=False)
    featured_image = Base64ImageField(required=False)
    tags = TagSerializer(many=True)
    categories = CategoryValueSerializer(many=True)
    post_type = PostTypeSerializer()
    post_status = PostStatusSerializer()

    class Meta:
        model = Post
        fields = ('id', 'post_status', 'title', 'slug', 'content', 'post_type', 'updated',
                  'headline', 'subtitle', 'shadowText', 'excerpt', 'seo_title', 'seo_description',
                  'categories', 'tags', 'readtime', 'featured_image')
        lookup_field = 'slug'  # Set the lookup_field here

class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
        
class PostUpdateSerializer(serializers.ModelSerializer):
    featured_image = Base64ImageField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'post_status', 'title', 'slug', 'content', 'post_type', 'updated',
                  'headline', 'subtitle', 'shadowText', 'excerpt', 'seo_title', 'seo_description',
                  'categories', 'tags', 'readtime', 'featured_image')
    
    
    
class RecentPostSerializer(serializers.ModelSerializer):
    categories = CategoryValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    updated = serializers.DateTimeField(format="%m-%d-%Y")
    post_type = PostTypeSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'updated', 'post_type',
                  'categories', 'tags', 'readtime', 'featured_image')

 