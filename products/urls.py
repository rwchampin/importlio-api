from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ScrapeAmazonViewSet
urlpatterns = [
     path('scrape/get-data/', views.get_data, name='get-data'),
     path('amazon/scrape-url/', ScrapeAmazonViewSet.as_view({ 'post': 'create' }), name='scrape-amazon-url'),
]
