from rest_framework import generics, viewsets, status
from .models import Post, Tag, Category, PostType
from .serializers import PostSerializer, RecentPostSerializer, TagSerializer, CategoryValueSerializer, PostTypeSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.core.files.base import ContentFile
import base64

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = PageNumberPagination

class PostCreateAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    # parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        # Convert base64-encoded image to a file
        featured_image_data = request.data.get('featured_image')
        if featured_image_data:
            image_format, image_data = featured_image_data.split(';base64,')
            image_extension = image_format.split('/')[-1]
            featured_image = ContentFile(base64.b64decode(image_data), name=f'featured_image.{image_extension}')
            request.data['featured_image'] = featured_image

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RecentPostListView(generics.ListAPIView):
    queryset = Post.objects.all()[:4]
    serializer_class = RecentPostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field = 'slug'
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.likes += 1
        post.save()
        serializer = PostSerializer(post)
        return Response({"post": serializer.data, "likes": post.likes}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.likes > 0:
            post.likes -= 1
            post.save()
            serializer = PostSerializer(post)
            return Response({"post": serializer.data, "likes": post.likes}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No likes to remove.", "likes": post.likes}, status=status.HTTP_400_BAD_REQUEST)
    
    
class PostsByCategoryView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field='slug'
    
    def get_queryset(self):
        category_name = self.request.query_params.get('category')
        if category_name:
            return Post.objects.filter(categories__name=category_name)
        else:
            return Post.objects.all()


class PostsByTagView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field='slug'
    
    def get_queryset(self):
        tag_pk = self.kwargs.get('slug')
        if tag_pk is not None:
            # Retrieve posts with the specified tag
            posts = Post.objects.filter(tags__slug=tag_pk)
            return posts
        return Post.objects.none()

        
        
class PostsByPostTypeView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field='slug'
    
    def get_queryset(self):
        post_type = self.request.query_params.get('post_type')
        if post_type:
            return Post.objects.filter(post_type__name=post_type)
        else:
            return Post.objects.all()
        
class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryValueSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
class PostTypeListView(generics.ListAPIView):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='name'