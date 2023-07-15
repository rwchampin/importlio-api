from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Registrant
from .serializers import RegistrantSerializer

# Create your views here.
class RegistrantViewSet(viewsets.ModelViewSet):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    permission_classes = [permissions.AllowAny]
    
    def