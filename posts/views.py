from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view

import base64
from .models import Post, Tag, Category, PostType, PostTopicIdeas
from .serializers import (
    PostSerializer, 
    TagSerializer, 
    CategorySerializer, 
    PostTypeSerializer, 
    PostCreateSerializer,
    PostTopicIdeasSerializer
)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    lookup_field = 'slug'
    queryset = Post.objects.all()
    
    
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def put(self, request, *args, **kwargs):
        # Convert base64-encoded image to a file
        featured_image_data = request.data.get('featured_image')
        if featured_image_data:
            image_format, image_data = featured_image_data.split(';base64,')
            image_extension = image_format.split('/')[-1]
            featured_image = ContentFile(base64.b64decode(image_data), name=f'featured_image.{image_extension}')
            request.data['featured_image'] = featured_image

        return self.update(request, *args, **kwargs)
    
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


class PostsByTagView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public

    def get_queryset(self):
        tag_slug = self.kwargs['tag']
        return Post.objects.filter(tags__slug=tag_slug)

class PostsByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(categories__slug=category)
    
class PostsByPostTypeView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        post_type_slug = self.kwargs['post_type']
        return Post.objects.filter(post_type__slug=post_type_slug)



class RecentPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        return Post.objects.filter(published__lte=timezone.now()).order_by('-updated')[:5]
    
class PostsByDate(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        date = self.kwargs['date']
        return Post.objects.filter(published__year=date.year, published__month=date.month, published__day=date.day)
    
    
class PostTopicIdeasViewSet(viewsets.ModelViewSet):
    serializer_class = PostTopicIdeasSerializer
    permission_classes = [AllowAny]  # Make this view public
    queryset = PostTopicIdeas.objects.all()
    
    
@api_view(['GET'])
def post_count(request):
    if request.method == 'GET':
        count = Post.objects.all().count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    
    
    
    
