from rest_framework import serializers
from django.core.files.base import ContentFile
import base64

 
from .models import Post, Tag, Category, PostType 

# Custom Serializer Fields
class CustomTagField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'slug': value.slug
        }

    def to_internal_value(self, data):
        return data['id']  # Only return the ID for saving

class CustomCategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'slug': value.slug
        }

    def to_internal_value(self, data):
        return data['id']  # Only return the ID for saving

class CustomPostTypeField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'slug': value.slug
        }

    def to_internal_value(self, data):
        return data['id']  # Only return the ID for saving

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

# Main Post Serializer
class PostSerializer(serializers.ModelSerializer):
    tags = CustomTagField(queryset=Tag.objects.all(), many=True)
    categories = CustomCategoryField(queryset=Category.objects.all(), many=True)
    post_type = CustomPostTypeField(queryset=PostType.objects.all())
    featured_image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Post
        fields = '__all__'
 
# Serializer for creating posts
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Individual serializers for Tag, Category, and PostType
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = '__all__'
