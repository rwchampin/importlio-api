from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ScrapeURLSerializer, ProductSerializer
import requests
from bs4 import BeautifulSoup
from .utils import extract_product_info
from rest_framework.decorators import api_view
from utils.scraping.get_proxy import get_proxy
from selectorlib import Extractor
from .proxy import ProxyManager

proxy_manager = ProxyManager()

# Create an Extractor by reading from the YAML file
# e = Extractor.from_yaml_file('selectors.yml')

# from .utils import get_title, get_description, get_price, get_reviews, get_images, get_availability, get_variants
class ScrapeAmazonViewSet(viewsets.ViewSet):
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = []
    
    def create(self, request):
        headers = ({'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})
        response = requests.get('https://www.amazon.com/s?k=laptops&crid=1BKE05LZEL0B2&sprefix=laptops%2Caps%2C87&ref=nb_sb_noss_1', headers=headers)
        import pdb; pdb.set_trace()
        if response.status_code == 200:
            product_list = extract_product_info(response.content)
            import pdb; pdb.set_trace()
            # soup = BeautifulSoup(response.content, "lxml")
            # title = get_title(soup)
            # description = get_description(soup)
            # price = get_price(soup)
            # reviews = get_reviews(soup)
            # images = get_images(soup)
            return Response(product_list, status=status.HTTP_200_OK)
            # Save to database
            # product = Product.objects.create(
            #     url=url,
            #     title=title,
            #     description=description,
            #     price=price,
            #     reviews=reviews,
            #     images=images,
            #     availability=availability,
            #     variants=variants
            # )
            # product_serializer = ProductSerializer(product)
            # return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to retrieve the page.'}, status=status.HTTP_400_BAD_REQUEST)







class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    


def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    print("Proxy used:", proxy)
    
    r = requests.get(url, headers=headers, proxies=proxy)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    
    return r

@api_view(['POST'])
def get_data(request):      
    
    url = request.data['url']
    
    res = scrape(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    
    
    return Response({'html': res.text })