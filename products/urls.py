from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ScrapeAmazonViewSet
urlpatterns = [
     path('amazon/scrape-url/', ScrapeAmazonViewSet.as_view({ 'post': 'create' }), name='scrape-amazon-url'),
]
