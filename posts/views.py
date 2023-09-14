from rest_framework import status
from .models import Post, Tag, Category, PostType, PostStatus
from .serializers import PostSerializer, RecentPostSerializer, TagSerializer, CategoryValueSerializer, PostTypeSerializer, PostStatusSerializer, PostUpdateSerializer, PostCreateSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.pagination import PageNumberPagination
from django.core.files.base import ContentFile
import base64
# import datetime
# from django.db.models import Q
from slugify import slugify


class PostCreateView(CreateAPIView):
    authentication_classes = []
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Post.objects.all()
    
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

class PostListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Post.objects.all()
    
# simple view for posts that will create a blank post if no data is provided 
class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Get the existing title and new title from the request data
        existing_title = instance.title
        new_title = request.data.get('title', existing_title)
        
        # Check if the title has changed
        if existing_title != new_title:
            instance.title = new_title
            instance.slug = slugify(new_title)  # Update the slug if the title has changed
        
        # Convert base64-encoded image to a file
        featured_image_data = request.data.get('featured_image')
        if featured_image_data:
            image_format, image_data = featured_image_data.split(';base64,')
            image_extension = image_format.split('/')[-1]
            featured_image = ContentFile(base64.b64decode(image_data), name=f'featured_image.{image_extension}')
            request.data['featured_image'] = featured_image
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class BlankPostCreateAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        # If no data is provided, create a blank post
        if not request.data:
            num_drafts = Post.objects.all().count() + 1
            title = f'Untitled Post {num_drafts}'
            new_post = Post.objects.create(title=title, slug=slugify(title), post_status_id=1, content='')
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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

 
    
 
    
class RecentPostListView(ListAPIView):
    # get the most recent 3 posts ith a status of published
    queryset = Post.objects.all()[:3]
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

 
    
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
        
class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryValueSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
class PostTypeListView(ListAPIView):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='name'
 
class PostStatusListView(ListAPIView):
    queryset = PostStatus.objects.all()
    serializer_class = PostStatusSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='slug'
     
 
def create_initial_post_data():
    # check if initial post data has already been created or create it
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post_types = PostType.objects.all()
    
    if categories and tags and post_types:
        pass
    else:
        blogCategories = [
            "Dropshipping Strategies",
            "E-commerce Tips",
            "Shopify Store Optimization",
            "Amazon Product Importing",
            "Product Sourcing Techniques",
            "Online Business Growth",
            "Shopify App Guides",
            "E-commerce Marketing",
            "SEO for E-commerce",
            "Business Automation"
        ]
        
        blogTags = [
            "Dropshipping Success",
            "Amazon Product Importer",
            "E-commerce Trends",
            "Shopify Apps",
            "Product Sourcing",
            "E-commerce SEO",
            "Online Store Tips",
            "Business Growth Strategies",
            "Shopify Store Setup",
            "E-commerce Marketing"
        ]
        
        postTypes = [
            "How-to Guides",
            "Tips and Tricks",
            "Case Studies",
            "Product Spotlights",
            "Industry News",
            "Success Stories",
            "Expert Interviews",
            "App Feature Updates",
            "E-commerce Insights",
            "Step-by-Step Tutorials"
        ]
        # Create initial post types
        for post_type in postTypes:
            PostType.objects.create(name=post_type)
            
        # Create initial categories
        for category in blogCategories:
            Category.objects.create(name=category)
            
        # Create initial tags
        for tag in blogTags:
            Tag.objects.create(name=tag)

        
# create_initial_post_data() 
def createPostStatusTypes():
    postStatusTypes = [
        "Draft",
        "Published",
        "Scheduled",
        "Archived",
        "Deleted"
    ]
    for postStatusType in postStatusTypes:
        PostStatus.objects.create(name=postStatusType)
    
# createPostStatusTypes()