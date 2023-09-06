from rest_framework import generics, status
from .models import Post, Tag, Category, PostType, PostStatus
from .serializers import PostSerializer, RecentPostSerializer, TagSerializer, CategoryValueSerializer, PostTypeSerializer, PostStatusSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.files.base import ContentFile
import base64
import datetime
from django.db.models import Q
from slugify import slugify

# simple view for posts that will create a blank post if no data is provided
class SimplePostCreateAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    # parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        # If no data is provided, create a blank post
        if not request.data:
            num_drafts = Post.objects.all().count() + 1
            title = f'Untitled Post {num_drafts}'
            new_post = Post.objects.create(title=title, slug=slugify(title))
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)
        
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
        # If no data is provided, create a blank post
        if not request.data:
            num_drafts = Post.objects.all().count() + 1
            title = f'Untitled Post {num_drafts}'
            new_post = Post.objects.create(title=title, slug=slugify(title))
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
 
    
class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
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
    
class RecentPostListView(generics.ListAPIView):
    # get the most recent 3 posts ith a status of published
    queryset = Post.objects.all().order_by('-updated')[:3]
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
 
class PostStatusListView(generics.ListAPIView):
    queryset = PostStatus.objects.all()
    serializer_class = PostStatusSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='name'   
    
class PostsByDateView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='updated'
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            return Post.objects.filter(updated__year=year, updated__month=month, updated__day=day)
        else:
            return Post.objects.all()
        
class PostsByMonthView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='updated'
    
    def get_queryset(self):
        #  if year is none, use current year
        if year is None:    
            year = datetime.now().year
        else:
            year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        if year and month:
            return Post.objects.filter(updated__year=year, updated__month=month)
        else:
            return Post.objects.all()
        
class PostsByYearView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='updated'
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        if year:
            return Post.objects.filter(updated__year=year)
        else:
            return Post.objects.all()
        
class PostsByDateRangeView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field='updated'
    
    def get_queryset(self):
        start_date = self.kwargs.get('start_date')
        end_date = self.kwargs.get('end_date')
        if start_date and end_date:
            return Post.objects.filter(updated__range=[start_date, end_date])
        else:
            return Post.objects.all()
        
class PostsDraftListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Adjust permissions as needed
    # get posts with status = draft
    def get_queryset(self):
        return Post.objects.filter(status='Draft')


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
     

class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Update permissions as needed
    lookup_field = 'pk'
    
    
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