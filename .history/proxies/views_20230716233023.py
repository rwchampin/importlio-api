import asyncio
from rest_framework import generics
from rest_framework.response import Response
from .models import Proxy
from .serializers import ProxySerializer
from proxybroker import Broker
from django.http import JsonResponse


class ProxyViewSet(models.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer


class ProxyCreateView(generics.CreateAPIView):
    serializer_class = ProxySerializer

    async def populate_proxies(self, limit):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        await asyncio.gather(broker.find(types=["HTTP", "HTTPS"], limit=limit))
        results = []
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            results.append(proxy)
        return results

    async def post(self, request, *args, **kwargs):
        limit = int(kwargs.get("limit"))
        proxies = await self.populate_proxies(limit)
        serializer = self.get_serializer(data=proxies, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
