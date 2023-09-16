from rest_framework import serializers
from django.core.files.base import ContentFile
import base64

 
from .models import Post, Tag, Category, PostType 
 
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
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        depth = 1
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True)
    post_type = PostTypeSerializer()
    updated = serializers.DateTimeField(format="%d-%m-%Y")
    featured_image = Base64ImageField(
        max_length=None, use_url=True,
    )
    

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'tags', 'categories', 'slug', 'read_time',  'updated', 'headline', 
            'post_type', 'featured_image', 'excerpt', 'subtitle', 'seo_title', 'seo_description', 'shadowText'  # Add other fields as needed
        ]


class UpdatePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'