from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from openai import OpenAI
from django.utils.text import slugify


from bs4 import BeautifulSoup
from ai.assistant import Assistant
import base64, os, requests

from .models import Post, Tag, Category, PostType, PostTopicIdeas, PostOutline, PostOutlineItem, PostRephrase, PostRephraseSegment
from .serializers import (
    PostSerializer, 
    PostPreviewSerializer,
    TagSerializer, 
    CategorySerializer, 
    PostTypeSerializer, 
    PostCreateSerializer,
    PostTopicIdeasSerializer,
    PostOutlineItemSerializer,
    PostOutlineSerializer
)
from importlio.settings import BASE_DIR

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    lookup_field = 'slug'
    queryset = Post.objects.filter(post_status='published').order_by('-updated')
    basename = 'post'  # Add this line to specify the basename
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'subtitle', 'content', 'tags__name', 'categories__name', 'post_type__name']
    
    def get_queryset(self):
        # check if limit query param is present
        limit = self.request.query_params.get('limit', None)
        post_status = self.request.query_params.get('post_status', None)
        
        queryset = Post.objects.all().order_by('-updated')
        
        # filter by post_status
        if post_status is not None:
            queryset = queryset.filter(post_status=post_status)
        
        # apply limit and reverse order if limit is specified
        if limit is not None:
            queryset = queryset[:int(limit)]
            
            
        return queryset
    
    # post or create
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
    
    # def list(self, request, *args, **kwargs):
    #     limit = request.query_params.get('limit', None)

    #     # order by updated
    #     if limit is not None:
    #         queryset = self.filter_queryset(self.get_queryset())[:int(limit)][::-1]
    #     else:
    #         queryset = self.filter_queryset(self.get_queryset())[::-1]
            

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

class PostPreviewViewSet(viewsets.ModelViewSet):
    serializer_class = PostPreviewSerializer
    permission_classes = [AllowAny]  # Make this view public
    lookup_field = 'slug'
    queryset = Post.objects.all().order_by('-updated')
    basename = 'post'  # Add this line to specify the basename
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'subtitle', 'content', 'tags__name', 'categories__name', 'post_type__name', 'seo_keywords']
    
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
    
# class PostCreateView(generics.CreateAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = PostCreateSerializer

#     def post(self, request, *args, **kwargs):
#         # Convert base64-encoded image to a file
#         featured_image_data = request.data.get('featured_image')
#         if featured_image_data:
#             image_format, image_data = featured_image_data.split(';base64,')
#             image_extension = image_format.split('/')[-1]
#             featured_image = ContentFile(base64.b64decode(image_data), name=f'featured_image.{image_extension}')
#             request.data['featured_image'] = featured_image

#         serializer = PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Post.objects.filter(post_status="published",tags__slug=tag_slug).order_by('-updated')

class PostsByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(post_status="published",categories__slug=category).order_by('-updated')
    
class PostsByPostTypeView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Make this view public
    def get_queryset(self):
        post_type_slug = self.kwargs['post_type']
        return Post.objects.filter(post_status="published", post_type__slug=post_type_slug).order_by('-updated')

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


class PostOutlineViewSet(viewsets.ModelViewSet):
    serializer_class = PostOutlineSerializer
    permission_classes = [AllowAny]  # Make this view public
    queryset = PostOutline.objects.all()
    
class PostOutlineItemViewSet(viewsets.ModelViewSet):
    serializer_class = PostOutlineItemSerializer
    permission_classes = [AllowAny]  # Make this view public
    queryset = PostOutlineItem.objects.all()
    

def parse_large_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    import pdb; pdb.set_trace()
    # get the html tag type of the html parent
    html_parent_tag = soup.html.parent.name
    
def concatenate_strings_with_commas(strings):
    if not strings:
        return ""
    
    concatenated_string = ",".join(strings)
    return concatenated_string
  
    
# api endpoint that receives a string of html
post_sources = [
    {
        "name": 'amazon',
        "url": "amazon.com"
    },{
        "name": 'autods',
        "url": "autods.com"
    }   
]

def get_post_source(url):
    for source in post_sources:
        # check if url contains the substring of the source url
        if source['url'] in url:
            return source['name']
        
    return None

@api_view(['POST'])
def rewrite_post(request):
    # get the url from the request or make None
    url = request.data.get('url', None)
    # get the domain from the url
    domain = get_post_source(url)
    
    
    # if valid domain, make an assistant
    if domain is None:
        return Response({'message': 'Invalid domain'}, status=status.HTTP_400_BAD_REQUEST)
    # create a new assistant
    assistant = Assistant()
    
    config = {
        "domain": domain,
        "url": url
    }
    post = assistant.uniquify(url)
    import pdb; pdb.set_trace()
    # get 3 random tags
    # tags = Tag.objects.order_by('?')[:3]
    # get 3 random categories
    # categories = Category.objects.order_by('?')[:3]
    # create a new post with the new content
    # featured_image_title = slugify(post['title']) + '.jpg'
    # img_content = post['featured_image']
    np = Post.objects.create(
        title=post['title'],
        subtitle=post['subtitle'],
        headline=post['headline'],
        excerpt=post['excerpt'],
        shadowText=post['shadowText'],
        seo_title=post['title'],
        seo_description=post['excerpt'],
        # remove the array brackets and add the csv to the seo keywords
        seo_keywords=post['seo_keywords'],
        content=post['content'],
        post_status='published',
        # get random post type
        post_type=PostType.objects.order_by('?').first(),
    )
    
    
    # post.featured_image.save(featured_image_title, ContentFile(img_content))
    # post.tags.set(tags)
    # post.categories.set(categories)
    np.save()
    
    # p = PostSerializer(post)
    
    return Response({'post': 'd'}, status=status.HTTP_200_OK)




 
    
    
# api endpoint that receives a string of html
@api_view(['GET'])
def make_posts(request):
    # get fulepath of ./posts.txt
    pages = []
    file_path = os.path.join(BASE_DIR, 'posts/posts.txt')
    # open the file posts.txr and loop through each line
    url = 'https://www.autods.com/blog/product-finding/amazon-best-selling-niches/'
    h = requests.get(url)
    html = h.text
    soup = BeautifulSoup(html, 'html.parser')
    # get title tag
    title = soup.title.string
    # get meta description tag
    description = soup.find('meta', attrs={'name': 'description'})
    
    # get post-content div
    post_content = soup.find('div', attrs={'class': 'post-content'})
    
    # turn post_content into a string
    post_content = str(post_content)
    
    prompt = 'the title: ' + title + '\n' + 'the description: ' + description['content']
    assistant = Assistant()   
    t = assistant.create_info(prompt) 
    import pdb; pdb.set_trace()
    # c = assistant.rephrase(post_content)
    import pdb; pdb.set_trace()
    # create a new post
   

    return Response({'post': p.data}, status=status.HTTP_200_OK)



 