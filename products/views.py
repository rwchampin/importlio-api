from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ScrapeURLSerializer, ProductSerializer
import requests
from bs4 import BeautifulSoup
from .utils import extract_product_info
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

