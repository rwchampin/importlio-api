from rest_framework import generics
from .models import Registrant
from .serializers import RegistrantSerializer

class RegistrantListCreateView(generics.ListCreateAPIView):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    authentication_classes = []
    permission_classes = []

class RegistrantDetailView(generics.RetrieveAPIView):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    authentication_classes = []
    permission_classes = []