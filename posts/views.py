from rest_framework import generics
from .models import Post
from .serializers import PostSerializer, RecentPostSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class RecentPostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-published_at")[:3]
    serializer_class = RecentPostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field = 'slug'
    
    
class PostsByCategoryView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed

    def get_queryset(self):
        category_name = self.request.query_params.get('category')
        if category_name:
            return Post.objects.filter(categories__name=category_name)
        else:
            return Post.objects.all()


class PostsByTagView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed

    def get_queryset(self):
        tag_name = self.request.query_params.get('tag')
        if tag_name:
            return Post.objects.filter(tags__name=tag_name)
        else:
            return Post.objects.all()
        
        
class PostsByPostTypeView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed

    def get_queryset(self):
        post_type = self.request.query_params.get('post_type')
        if post_type:
            return Post.objects.filter(post_type__name=post_type)
        else:
            return Post.objects.all()