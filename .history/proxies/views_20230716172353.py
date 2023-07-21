from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .models import Proxy
from .serializers import ProxySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import populate_proxies_from_api

class ProxyViewset(viewsets.ModelViewSet):
	queryset = Proxy.objects.all()
	serializer_class = ProxySerializer




class ProxyPopulateView(APIView):
    def post(self, request):
        if populate_proxies_from_api():
            return Response({'message': 'Proxies populated successfully'}, status=201)
        else:
            return Response({'message': 'Failed to populate proxies'}, status=500)
