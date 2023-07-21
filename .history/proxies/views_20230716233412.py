
from rest_framework import  viewsets

from .models import Proxy
from .serializers import ProxySerializer
from proxybroker import Broker

from rest_framework.decorators import action


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer

    @action(detail=False, methods=["post"])
    def populate(self, request, *args, **kwargs):
        protocols = request.data.get("protocols")
        limit = int(request.data.get("limit"))
        countries = request.data.get("countries")
        anonymity_levels = request.data.get("anonymity_levels")
        
        broker = Broker()
        broker.find(
            types=[protocols],
            limit=limit,
            countries=[countries],
            anonymity_levels=[anonymity_levels],
            )
        results = []
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            results.append(proxy)
        serializer = self.get_serializer(data=results, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers

# class ProxyCreateView(generics.CreateAPIView):
#     serializer_class = ProxySerializer

#     async def populate_proxies(self, limit):
#         proxies = asyncio.Queue()
#         broker = Broker(proxies)
#         await asyncio.gather(broker.find(types=["HTTP", "HTTPS"], limit=limit))
#         results = []
#         while True:
#             proxy = await proxies.get()
#             if proxy is None:
#                 break
#             results.append(proxy)
#         return results

#     async def post(self, request, *args, **kwargs):
#         limit = int(kwargs.get("limit"))
#         proxies = await self.populate_proxies(limit)
#         serializer = self.get_serializer(data=proxies, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=201, headers=headers)
