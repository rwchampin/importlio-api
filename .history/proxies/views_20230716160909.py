from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .models import Proxy
from .serializers import ProxySerializer

class ProxyViewset(viewsets.ModelViewSet):
	queryset = Proxy.objects.all()
	serializer_class = ProxySerializer


