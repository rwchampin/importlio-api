from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny  # Import AllowAny permission class

from .utils import WebScraper  # Import the WebScraper class from your utils module

@api_view(['GET'])  # Use the appropriate HTTP method for your view
@permission_classes([])  # Set any permissions your view requires here
@authentication_classes([])  # Set any authentication your view requires here
def get_oberlo(request):
    url = 'https://www.oberlo.com/blog/'
    button_xpath = "//button[text()='Show More']"
    scraper = WebScraper(url, button_xpath)

    try:
        html_content = scraper.scrape_page()
        return JsonResponse({'html_content': html_content}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



 