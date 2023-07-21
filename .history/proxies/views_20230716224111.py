from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .models import Proxy
from .serializers import ProxySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio
from proxybroker import Broker
import requests

# from .utils import populate


# def populate():
#     url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
#     import pdb

#     pdb.set_trace()
#     response = requests.get(url)
#     if response.status_code == 200:
#         proxies_data = response.json().get("data", [])
#         proxies = []
#         for proxy_data in proxies_data:
#             # if validate_proxy(proxy_data):
#             proxy = Proxy(
#                 ip=proxy_data.get("ip"),
#                 port=proxy_data.get("port"),
#                 country=proxy_data.get("country"),
#                 anonymity=proxy_data.get("anonymity"),
#                 protocols=proxy_data.get("protocols"),
#                 last_checked=proxy_data.get("lastChecked"),
#             )
#             proxies.append(proxy)

#             Proxy.objects.bulk_create(proxies)
#         return True
#     return False


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    permission_classes = []


class ProxyPopulationView(APIView):
    async def fetch_proxies(self, types, limit):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        await asyncio.gather(
            broker.find(types=types, limit=limit), return_exceptions=True
        )
        results = []
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            results.append(
                {
                    "host": proxy.host,
                    "port": proxy.port,
                    "type": proxy.types,
                }
            )
        return results

    def get(self, request):
        types = ["HTTP", "HTTPS"]  # Specify the types of proxies you want to fetch
        limit = self.request["limit"]  # Specify the number of proxies you want to fetch

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self.fetch_proxies(types, limit))

        return Response(results)


# def validate_proxy(proxy):
#     checker = ProxyChecker()
#     result = checker.check_proxy(proxy)

#     # Process the result and extract relevant information
#     country = result.get("country")
#     country_code = result.get("country_code")
#     protocols = result.get("protocols")
#     anonymity = result.get("anonymity")
#     timeout = result.get("timeout")

#     # Perform additional checks or store the result as needed
#     if protocols:
#         # Do something with the protocols
#         pass

#     if anonymity == "Elite":
#         # Proxy is elite, perform additional actions
#         pass

#     # Return the result or perform further processing
#     return result
