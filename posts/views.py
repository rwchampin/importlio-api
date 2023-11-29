from django.utils import timezone
from rest_framework import viewsets, generics, status, mixins, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes, action

import base64
from .models import Post, Tag, Category, PostType, PostTopicIdeas
from .serializers import (
    PostSerializer, 
    TagSerializer, 
    CategorySerializer, 
    PostTypeSerializer, 
    PostCreateSerializer,
    PostTopicIdeasSerializer,
)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    lookup_field = 'slug'
    queryset = Post.objects.all()
    
    def get_queryset(self):
        # check if limit query param is present
        limit = self.request.query_params.get('limit', None)
        
        # order by updated && if post_status is published
        if limit is not None:
            # queryset = Post.objects.all()[:int(limit)][::-1]
            queryset = Post.objects.filter(post_status='published')[:int(limit)][::-1]
        else:
            queryset = Post.objects.filter(post_status='published')[::-1]
            
        return queryset
    
    # def list(self, request, *args, **kwargs):
    #     limit = request.query_params.get('limit', None)

    #     # order by updated
    #     if limit is not None:
    #         queryset = self.filter_queryset(self.get_queryset())[:int(limit)][::-1]
    #     else:
    #         queryset = self.filter_queryset(self.get_queryset())[::-1]
            

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
      
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
        return Post.objects.filter(tags__slug=tag_slug).order_by('-updated')

class PostsByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(categories__slug=category).order_by('-updated')
    
class PostsByPostTypeView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        post_type_slug = self.kwargs['post_type']
        return Post.objects.filter(post_type__slug=post_type_slug).order_by('-updated')

class PostsByDate(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        date = self.kwargs['date']
        return Post.objects.filter(published__year=date.year, published__month=date.month, published__day=date.day).order_by('-updated')
    
class PostTopicIdeasViewSet(viewsets.ModelViewSet):
    serializer_class = PostTopicIdeasSerializer
    permission_classes = [AllowAny]  # Make this view public
    queryset = PostTopicIdeas.objects.all()
    
    
@api_view(['GET'])
def post_count(request):
    if request.method == 'GET':
        count = Post.objects.all().count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    
    
    
def create_post_topic_ideas():
    default_topic_ideas = [
        "The Ultimate Shopify Dropshipping Guide",
        "Top 20 Best-Selling Oberlo Dropshipping Products of 2020",
        "The Ultimate Guide to AliExpress Dropshipping",
        "How to Avoid Counterfeit Goods on AliExpress",
        "The Best Dropshipping Courses You Need to Take in 2023",
        "How to Handle Refunds and Returns as a Dropshipper",
        "The 7 Best Ecommerce Niches to Target in 2023",
        "Etsy Dropshipping: The Ultimate Guide for Dropshipping on Etsy",
        "Automated Dropshipping: Every Way to Automate Your Business",
        "How Much Does it Cost to Launch a Dropshipping Store?",
        "Dropshipping Vs Affiliate Marketing: Which is More Profitable?",
        "Alibaba Dropshipping: How to Safely Dropship From Alibaba (2023)",
        "How to Start a Dropshipping Business in 2023",
        "How to Source Products (+10 Top Sourcing Websites and Apps) [2023]",
        "13 Top Print-on-Demand Companies (and How to Choose One) in 2023",
        "Wix vs. Shopify: Which Is Best For Your Needs? (2023)",
        "BigCommerce vs. Shopify (2023): Which is Best for Your Business?",
        "How to Sell Preorders for Upcoming and Out-of-Stock Products",
        "How to Find Clothing Manufacturers for Your Business",
        "eBay Dropshipping: The Ultimate Guide to Dropshipping on eBay",
        "6 Best Dropshipping Suppliers and How to Choose The Right One",
        "AliExpress Standard Shipping: How Long It Really Takes (Case Study)",
        "Amazon Dropshipping Guide",
        "Dropshipping Niches That Are Steady, Not Trendy",
        "What Is ePacket Delivery?",
        "Test Orders Are So Important for Dropshippers. Here's Why.",
        "How to Find the Perfect Dropshipping Products",
        "The 8 Best Dropshipping Websites for Your New Ecommerce Store ",
        "How to Use Shopify: A Quick and Easy Shopify Tutorial (2023)",
        "Top 8 Amazon Competitors To Know (2023)",
        "Managing Your AliExpress Dropshipping Orders | FAQs (January, 2021)",
        "Shopify vs. Squarespace: Which Is the Best Option for You?",
        "15 Pricing Strategies to Boost Your Sales (With Examples)",
        "Best Sports Products to Sell in 2021",
        "EU's New 2021 VAT Changes and Your Dropshipping Business: What You Need to Know",
        "Best Dropshipping Products to Sell in Spring 2021",
        "Print On Demand Vs. AliExpress Dropshipping: Which is More Profitable?",
        " Dropshipping vs. Private Label: Which Should You Choose?",
        "Online General Store: 5 Products From a Successful Entrepreneur",
        "Dropshipping on Any Budget With Kamil Sattar",
        "The Pathway From Full-Time Work To Your Own Dropshipping Business",
        "Branded Niche Store: Why It Works and Six Reasons To Start One",
        "The 45 Best Podcasts to Help You Get Ahead in 2021",
        "How Will Chinese New Year 2021 Affect Your Store",
        "Product Watch: Cable Manager",
        "Fastest Way To Start a Dropshipping Business (Plus Free Shortcuts)",
        "21 Winning Niches To Start Selling for 2021",
        "10 Best-Selling Oberlo Products of All Time",
        "Start Dropshipping: Things to Know Before You Do",
        "Hottest New Products To Sell Before The Holidays",
        "The Secret to Dropshipping Profit? Consistency.",
        "How to Find Reliable Suppliers For Your Dropshipping Business",
        "Avoiding the Most Common Mistakes Made by New Dropshippers",
        "16 Best-Selling Dropshipping Products Around the World",
        "Finding Success With a Niche Product",
        "What Should You Do About Long Shipping Times",
        "Dropshipping on Any Budget: An Interview with Ecom King",
        "15 Best Selling Products in the Coronavirus Economy",
        "Seven Dropshipping Secrets Discovered on TikTok",
        "The Entrepreneur Who Left a Cushy Tech Job To Be His Own Boss",
        "This Entrepreneur's One Product Store Made $680k in Three Months. Then He Shut it All Down.",
        "How Emotions Can Lead To a Business Blind Spot",
        "Wholesale Ted vs Oberlo: Print-On-Demand or Dropshipping",
        "Free Shopify Dropshipping Tutorial for Beginners",
        "Six Tips From A Long-Time Dropshipper That All Beginners Should Hear",
        "The Path to Launching a Million-Dollar Store",
        "10 Dropshipping Myths That Need to Be Debunked for Good",
        "How This Couple Created a Sustainable Business While Working Full-Time",
        "How to Start Dropshipping in 2020: Your All Killer, No Filler Guide",
        "The Ultimate Guide to Building Powerful Product Pages",
        "100+ Best Products to Sell in 2020",
        "Dropshipping 101: Ecommerce Without Inventory",
        "Free Traffic: No-Cost Ways to Promote Your Online Store",
        "The Definitive Guide to Wholesale",
        "50 Ways to Get Sales With Dropshipping",
        "21 Days to Your First Dropshipping Sale",
        "Here Are the Fastest Growing Categories and Highest Selling Products Right Now",
        "Getting Real About Dropshipping",
        "How to Tackle Delivery Times in Dropshipping",
        "9 Products With Fast Shipping to Sell in 2020",
    ]

    if PostTopicIdeas.objects.count() == 0:
        for topic in default_topic_ideas:
            PostTopicIdeas.objects.create(topic=topic)
