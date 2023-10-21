from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .models import Email, MarketingList, MarketingStatistic
from .serializers import EmailSerializer, PreviewMarketingListSerializer, MarketingListSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import csv

# Create your views here.
from .utils import scrape_google_search, get_google_search_results


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (AllowAny,)

    
class PreviewMarketingListViewSet(viewsets.ModelViewSet):
    queryset = MarketingList.objects.all()
    serializer_class = PreviewMarketingListSerializer
    permission_classes = (AllowAny,)
    
class MarketingListViewSet(viewsets.ModelViewSet):
    queryset = MarketingList.objects.all()
    serializer_class = MarketingListSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
# class EmailListCreateView(generics.ListCreateAPIView):
#     queryset = Email.objects.all()
#     serializer_class = EmailSerializer
#     permission_classes = (AllowAny,)
    
#     def get_queryset(self):
#         queryset = Email.objects.all()
#         niche = self.request.query_params.get('niche', None)
#         if niche is not None:
#             queryset = queryset.filter(niche__name=niche)
#         return queryset
    
#     def create(self, request, *args, **kwargs):
#         query = request.data.get('query', None)
#         parsed_html = scrape_google_search(query, 200)
#         import pdb; pdb.set_trace()
#         return super().create(request, *args, **kwargs)
    
    
# def create_marketing_niches():
#     niches = [
#         "Fitness and Health Enthusiasts",
#         "Outdoor Adventure and Hiking",
#         "Yoga and Meditation Practitioners",
#         "Vegan and Plant-Based Dieters",
#         "Pet Owners and Animal Lovers",
#         "Parents of Newborns",
#         "Gamers and Gaming Enthusiasts",
#         "Home Improvement and DIY Hobbyists",
#         "Travel and Adventure Seekers",
#         "Beauty and Skincare Enthusiasts",
#         "Foodies and Gourmet Cooking",
#         "Sustainable and Eco-Friendly Consumers",
#         "Personal Finance and Investment",
#         "Fashion and Style Aficionados",
#         "Tech Geeks and Gadgets Lovers",
#         "Photography Enthusiasts",
#         "Coffee and Tea Connoisseurs",
#         "Bookworms and Bibliophiles",
#         "Fitness for Seniors",
#         "Natural and Organic Product Consumers",
#         "Cyclists and Bike Enthusiasts",
#         "CrossFit and Weightlifting",
#         "Wine and Wine Tasting",
#         "Parents of Toddlers",
#         "Freelancers and Remote Workers",
#         "Home Decor and Interior Design",
#         "Nutrition and Supplements",
#         "Gardening and Horticulture",
#         "DIY Crafters and Artisans",
#         "Sustainable Fashion and Clothing",
#         "Personal Development and Self-Help",
#         "Music and Musician Community",
#         "CrossFit and HIIT Workouts",
#         "Keto and Low-Carb Dieters",
#         "Coffee at Home Brewing",
#         "Car Enthusiasts and Auto Lovers",
#         "Digital Nomads and Travelers",
#         "Collectors (e.g., Coins, Stamps)",
#         "Survivalists and Preppers",
#         "Wine Collectors and Enthusiasts",
#         "Mindfulness and Stress Relief",
#         "Vintage and Retro Fashion",
#         "Tech-Savvy Parents",
#         "Knitting and Crocheting",
#         "Vegetarian Diet Followers",
#         "Organic and Sustainable Farming",
#         "Natural Parenting and Attachment",
#         "Health and Wellness Coaches",
#         "Mountain Climbing and Adventure",
#         "Personal Finance Bloggers",
#         "Skincare for Specific Skin Types",
#         "Smart Home and IoT Enthusiasts",
#         "Fantasy Sports and Betting",
#         "Pet Groomers and Trainers",
#         "Cooking and Baking for Beginners",
#         "RV and Camping Enthusiasts",
#         "Freelance Writers and Bloggers",
#         "Antique Collectors and Resellers",
#         "Tiny House Living",
#         "Herbal Remedies and Natural Healing",
#         "Personal Branding and Influencers",
#         "Astronomy and Stargazing",
#         "Skiing and Snowboarding",
#         "Paddleboarding and Water Sports",
#         "Hiking Gear and Equipment",
#         "Digital Artists and Illustrators",
#         "Sustainable Living Blogs",
#         "Drone Enthusiasts and Pilots",
#         "Minimalism and Decluttering",
#         "Sustainable Energy and Solar",
#         "Craft Beer and Microbreweries",
#         "Paleo Diet and Lifestyle",
#         "Graphic Designers and Creatives",
#         "Motorcyclists and Bikers",
#         "Mindful Parenting and Attachment",
#         "Science Fiction and Fantasy Fans",
#         "Beach and Coastal Living",
#         "Language Learning and Polyglots",
#         "Fitness Equipment and Gear",
#         "Personal Finance for Millennials",
#         "Sustainable Transportation",
#         "Geocaching and Treasure Hunting",
#         "3D Printing and Makers",
#         "Vintage Car Restoration",
#         "Alternative Medicine and Holistic Health",
#         "Rock Climbing and Bouldering",
#         "Backyard Farming and Homesteading",
#         "DIY Electronics and Robotics",
#         "Clean Beauty and Skincare",
#         "Film Photography and Analog",
#         "Hiking and Camping Gear Reviews",
#         "Collectible Toys and Figurines",
#         "Astronomy and Astrophotography",
#         "Watercolor Painting and Art",
#         "Surfing and Surfboard Enthusiasts",
#         "Off-Grid Living and Sustainability",
#         "Tiny House Builders and Enthusiasts",
#         "Vinyl Record Collectors",
#         "Urban Gardening and Hydroponics",
#         "Board Game Enthusiasts"
#     ]

#     if Niche.objects.all().count() > 0:
#         return
#     for niche in niches:
#         Niche.objects.create(name=niche)

def generate_google_query(keywords):
    # Prepare the base Google search URL
    base_url = "http://www.google.com/search?q="
    
    # Create the query by joining keywords with " AND " and adding other conditions
    query = " AND ".join(keywords)
    query = f'"{query}" AND "%40gmail.com" -intitle:"profiles" -inurl:"dir/+"+site:www.linkedin.com/in/+OR+site:www.linkedin.com/pub/'
    
    # Combine the base URL with the query
    search_url = base_url + query
    
    return search_url

@api_view(['POST'])
def get_data(request):
    
    if request.method == 'POST':
        query = request.data.get('query', None);
        limit = request.data.get('limit', -1);
        if query is not None:
            # url = generate_google_query(query, limit)
            email_json = scrape_google_search()
            return JsonResponse({"t": email_json})
        else:
            # throw error
            raise Exception('No query fields provided')
        
        
        # AIzaSyAKA_fLIUE_VQkdD95yg93oADg2vS0Uhcc
        
@api_view(['POST'])
def bulk_create_emails(request):
    if request.method == 'POST':
        niche = request.data.get('niche', None)

        # get or create niche
        if niche is not None:
            niche = Niche.objects.get_or_create(name=niche)[0]
        else:
            # throw error
            raise Exception('No niche provided')
            
        emails = request.data.get('emails', None)
        if emails is not None and niche is not None:
            for email in emails:
                # check if email exists
                if Email.objects.filter(email=email).exists():
                    e = Email.objects.get(email=email)
                    # add niche to email
                    e.niche.add(niche)
                else:
                    e = Email.objects.create(email=email)
                    e.niche.add(niche)
                    e.save()
            return JsonResponse({"success": True})
        else:
            # throw error
            raise Exception('No emails provided')
        
        
# class EmailListView(generics.ListAPIView):
    # queryset = Email.objects.all()
    # serializer_class = EmailSerializer
    # permission_classes = (AllowAny,)
    
    # def get_queryset(self):
    #     queryset = Email.objects.all()
    #     niche = self.request.query_params.get('niche', None)
    #     if niche is not None:
    #         queryset = queryset.filter(niche__name=niche)
    #     return queryset
    
# class NicheListView(generics.ListAPIView):
#     queryset = Niche.objects.all()
#     serializer_class = NicheSerializer
#     permission_classes = (AllowAny,)
    
#     def get_queryset(self):
#         queryset = Niche.objects.all()
#         return queryset
    
    
# @api_view(['POST'])
# def download_emails_by_niche(request):
#     if request.method == 'POST':
#         niche = request.data.get('niche', None)
#         if niche is None:
#             # throw error
#             raise Exception('No niche provided')
#     # Query the database to get emails by niche
#     emails = Email.objects.filter(niche=niche).values_list('email', flat=True)

#     # Create a CSV response
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="{niche}_emails.csv"'

#     # Create a CSV writer
#     writer = csv.writer(response)

#     # Write the CSV header (if needed)
#     # writer.writerow(['Email'])

#     # Write the email data to the CSV file
#     for email in emails:
#         writer.writerow([email])

#     return response



# def populate_statistics():
#     # Create niches for each target audience
#     genz = Niche.objects.get_or_create(name="Gen Z")[0]
#     b2b = Niche.objects.get_or_create(name="B2B Decision Makers")[0]
#     health = Niche.objects.get_or_create(name="Health and Wellness Enthusiasts")[0]
#     tech = Niche.objects.get_or_create(name="Tech Enthusiasts")[0]


    
    # Create and attach statistics to their respective niches
    statistics_data = [
        # ("E-commerce Shopping", "Gen Z is a digitally native generation with significant e-commerce spending habits. In 2021, Gen Z contributed to the $586.92 billion global e-commerce sales, representing a lucrative market segment.", genz),

        # ("Sustainability Preferences", "Gen Z values sustainability and eco-friendly products. Businesses aligning with sustainable practices can attract Gen Z consumers, who influence buying decisions within their households.", genz),

        # ("Social Media Advertising","Gen Z is highly active on social media platforms, making social media advertising an effective way to reach them. Businesses can tap into this market by investing in social media marketing campaigns.", genz),

        # ("Online Streaming Services", "Gen Z is a key demographic for online streaming platforms. Streaming services that offer diverse content can capture this audience, contributing to subscription revenue growth.", genz),

        # ("Personalized Shopping Experiences", "Gen Z appreciates personalized shopping experiences. Businesses that implement AI-driven personalization can increase customer engagement and sales among Gen Z consumers.", genz),

        
        ("Cloud Computing Services", "B2B decision-makers are adopting cloud computing services. The global cloud computing market is projected to reach $832.1 billion by 2025, driven by businesses' digital transformation efforts.", b2b),

        ("SaaS Solutions", "Software as a Service (SaaS) solutions are in high demand among businesses. The SaaS market is estimated to grow to $145.3 billion in 2022, making it a competitive space for SaaS providers.", b2b),

        ("Cybersecurity Investments", "B2B decision-makers prioritize cybersecurity investments. The global cybersecurity market's growth presents opportunities for cybersecurity vendors serving enterprises.", b2b),

        ("Remote Work Solutions", "The remote work trend has led to increased demand for remote work solutions and collaboration tools, with the market projected to reach $16.6 billion by 2026.", b2b),

        ("Data Analytics and AI", "Businesses are investing in data analytics and AI solutions to gain insights and improve decision-making. The global AI in the B2B market is expected to reach $20.6 billion by 2027.", b2b),
       

        
        ("Nutritional Supplements Market", "Health and wellness enthusiasts contribute to the growth of the nutritional supplements market. It was valued at $140.3 billion in 2020 and is expected to expand further.", health),
        ("Fitness Equipment Sales", "Home fitness equipment sales surged during the COVID-19 pandemic. The global fitness equipment market is estimated to reach $14.6 billion by 2028, driven by health-conscious consumers.", health),
        ("Mental Health Services", "The focus on mental health and well-being has led to increased demand for mental health services and digital wellness platforms. The mental health market is projected to reach $336.7 billion by 2028.", health),
        ("Healthy Food and Beverages", "Health-conscious consumers are driving the market for healthy and organic food and beverages. The global organic food market is expected to grow at a CAGR of 16.5% by 2028.", health),
        ("Wearable Health Tech", "Wearable health technology, such as fitness trackers and smartwatches, is thriving. The wearable fitness technology market is anticipated to reach $48.2 billion by 2027, presenting opportunities for health tech businesses.", health),

        
        ("Consumer Electronics Spending", "Tech enthusiasts consistently invest in the latest gadgets and consumer electronics. Global consumer electronics spending exceeded $1.7 trillion in 2020, offering a substantial market for tech businesses.", tech),
        ("Smart Home Adoption", "The smart home market is growing rapidly, with tech-savvy consumers embracing smart devices. In 2021, the global smart home market size was valued at $90.96 billion, driven by demand for connected devices.", tech),
        ("AI and Automation Solutions", "Tech enthusiasts are early adopters of AI and automation solutions. The AI market is expected to reach $190 billion by 2025, creating opportunities for businesses offering AI-powered products and services.", tech),
        ("Cybersecurity Services", "With increasing cyber threats, tech enthusiasts prioritize cybersecurity. The global cybersecurity market is projected to reach $248.6 billion by 2023, making it a lucrative sector for cybersecurity firms.", tech),
        ("Tech Content Creation", "Tech enthusiasts create and consume tech-related content. Tech YouTubers, bloggers, and influencers are in high demand, with some earning substantial incomes through sponsored content and affiliate marketing.", tech),
    ]

    # for name, description, niche in statistics_data:
    #     MarketingStatistic.objects.get_or_create(
    #         name=name,
    #         description=description,
    #         niche=niche
    #     )

# Call the function to populate the statistics
# populate_statistics()
