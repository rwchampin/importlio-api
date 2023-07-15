from django.urls import path, include
from rest_framework import routers

from .views import RegistrantViewSet, RegisterViewSet

urlpatterns = [
    path('registrants/', RegistrantViewSet.as_view({'get': 'list'}), name='registrant-list'),
    path('register/', RegisterViewSet.as_view({'post': 'register'}), name='register'),
]
