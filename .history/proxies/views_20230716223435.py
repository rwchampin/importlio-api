from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .models import Proxy
from .serializers import ProxySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

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


class ProxyCreateView(APIView):
    def post(self, request):
        if populate():
            return Response({"message": "Proxies populated successfully"}, status=201)
        else:
            return Response({"message": "Failed to populate proxies"}, status=500)
