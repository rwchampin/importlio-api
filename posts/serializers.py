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
    class Meta:
        model = Category
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = '__all__'

class PostStatusSerializer(serializers.ModelSerializer):
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
    published = serializers.DateTimeField(format="%m-%d-%Y", required=False)
    updated = serializers.DateTimeField(format="%m-%d-%Y", required=False)
    featured_image = Base64ImageField(required=False)
    tags = TagSerializer(many=True, read_only=True)
    categories = CategoryValueSerializer(many=True, read_only=True)
    post_type = PostTypeSerializer(read_only=True)
    post_status = PostStatusSerializer(read_only=True)
    
    lookup_field = 'slug'
    pagination_class = []
    class Meta:
        model = Post
        fields = ( 'id', 'post_status', 'title', 'slug', 'content', 'post_type','published','updated','headline', 'subtitle', 'shadowText', 'excerpt', 'seo_title', 'seo_description',
                  'categories', 'tags', 'readtime', 'likes', 'dislikes', 'featured_image')
    def get_post_type(self, obj):
        return obj.post_type.name if obj.post_type else None
    
class RecentPostSerializer(serializers.ModelSerializer):
    queryset = Post.objects.filter(post_status__name="Draft").order_by('-published')[:3]
    categories = CategoryValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    published = serializers.DateTimeField(format="%m-%d-%Y")
    updated = serializers.DateTimeField(format="%m-%d-%Y")


    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'published', 'updated', 'post_type',
                  'categories', 'tags', 'readtime', 'likes', 'dislikes', 'featured_image')

 