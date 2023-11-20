from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
     path('scrape/get-data/', views.get_data, name='get-data'),
     path('', include(router.urls)),
]
