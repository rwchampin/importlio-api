from rest_framework import serializers
from django.core.files.base import ContentFile
import base64


from .models import Post, Tag, Category, PostType, PostTopicIdeas, PostOutline, PostOutlineItem

# For handling Base64 encoded images


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


# Serializer for creating posts
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Individual serializers for Tag, Category, and PostType


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        depth = 1
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        depth = 1
        fields = '__all__'


class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        depth = 1
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    categories = CategorySerializer(many=True, required=False)
    post_type = PostTypeSerializer(required=False)
    updated = serializers.DateTimeField(required=False)
    updated_pretty = serializers.SerializerMethodField(
        method_name='get_updated_pretty', required=False)

    published = serializers.DateTimeField(required=False)
    published_pretty = serializers.SerializerMethodField(
        method_name='get_published_pretty', required=False)

    def get_updated_pretty(self, obj):
        if obj.updated:
            return obj.updated.strftime("%d-%m-%Y")
        return None

    def get_published_pretty(self, obj):
        if obj.published:
            return obj.published.strftime("%d-%m-%Y")
        return None
    featured_image = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    # mobile_image = Base64ImageField(
    #     max_length=None, use_url=True, required=False
    # )
    # tablet_image = Base64ImageField(
    #     max_length=None, use_url=True, required=False
    # )
    # desktop_image = Base64ImageField(
    #     max_length=None, use_url=True, required=False
    # )

    class Meta:
        model = Post
        fields = '__all__'
        # fields = [
        #     'id', 'title', 'content', 'tags', 'categories', 'slug', 'read_time',  'updated', 'headline', 'published', 'word_count',
        #     'post_type', 'excerpt', 'subtitle', 'seo_title', 'seo_description', 'shadowText', 'shadow_text_theme', "title_text_theme", "subtitle_text_theme", "headline_text_theme",
        #     "updated_pretty", "published_pretty", "seo_keywords", 'tablet_image', 'desktop_image', 'mobile_image', 'featured_image'
        #     # Add other fields as needed
        # ]


class PostPreviewSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    categories = CategorySerializer(many=True, required=False)
    post_type = PostTypeSerializer(required=False)
    updated = serializers.DateTimeField(required=False)
    updated_pretty = serializers.SerializerMethodField(
        method_name='get_updated_pretty', required=False)

    published = serializers.DateTimeField(required=False)
    published_pretty = serializers.SerializerMethodField(
        method_name='get_published_pretty', required=False)

    def get_updated_pretty(self, obj):
        if obj.updated:
            return obj.updated.strftime("%d-%m-%Y")
        return None

    def get_published_pretty(self, obj):
        if obj.published:
            return obj.published.strftime("%d-%m-%Y")
        return None
    
    featured_image = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'id', 'tags', 'title', 'slug', 'read_time', 'updated','updated_pretty', 'headline', 'published', 'published_pretty', 'word_count', 'post_type', 'excerpt', 'subtitle', 'shadowText', "featured_image", "categories"
        ]


class UpdatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostTopicIdeasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTopicIdeas
        fields = '__all__'


class PostOutlineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOutlineItem
        fields = '__all__'


class PostOutlineSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = PostOutline
        fields = '__all__'


