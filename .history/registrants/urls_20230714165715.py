from django.urls import path, include
from rest_framework import routers

from .views import RegistrantViewSet, RegisterViewSet

router = routers.DefaultRouter()
router.register(r'registrants', RegistrantViewSet, basename='registrant')

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post': 'register'}), name='register'),
]
