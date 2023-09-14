from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.core.files.base import ContentFile
import base64
from .models import Post, Tag, Category, PostType
from .serializers import (
    PostSerializer, 
    TagSerializer, 
    CategorySerializer, 
    PostTypeSerializer, 
    PostCreateSerializer
)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
class PostCreateView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PostCreateSerializer

    def post(self, request, *args, **kwargs):
        # Convert base64-encoded image to a file
        featured_image_data = request.data.get('featured_image')
        if featured_image_data:
            image_format, image_data = featured_image_data.split(';base64,')
            image_extension = image_format.split('/')[-1]
            featured_image = ContentFile(base64.b64decode(image_data), name=f'featured_image.{image_extension}')
            request.data['featured_image'] = featured_image

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]  # Make this view public

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Make this view public

class PostTypeViewSet(viewsets.ModelViewSet):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer

class RecentPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public

    def get_queryset(self):
        return Post.objects.filter(published__lte=timezone.now()).order_by('-published')[:5]

class PostsByTagView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        return Post.objects.filter(tags__slug=tag_slug)

class PostsByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        cat_slug = self.kwargs['cat_slug']
        return Post.objects.filter(categories__slug=cat_slug)

# ... (existing code for create_initial_post_data)

class RecentPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        return Post.objects.filter(published__lte=timezone.now()).order_by('-published')[:5]