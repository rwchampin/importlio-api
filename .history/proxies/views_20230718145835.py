from rest_framework import viewsets, decorators
from rest_framework.response import Response
from .models import Proxy
from .serializers import ProxySerializer
import requests

judge = "https://httpbin.org/ip"


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    authentication_classes = []
    permission_classes = []

    def validate_proxy(self, proxy):
        try:
            response = requests.get(judge, proxies=proxy, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(e)
            return False

    @decorators.action(detail=False, methods=["post"])
    def populate(self, request):
        limit = request.query_params.get("limit")
        if not limit:
            return Response({"detail": "Limit must be provided."}, status=400)

        limit = int(limit)
        proxy_json = self.get_proxy_json(limit=limit)

        if proxy_json:
            results = []

            for proxy in proxy_json:
                proxy_data = {
                    "ip": proxy["ip"],
                    "port": proxy["port"],
                    "country": proxy["country"],
                    "last_checked": proxy["lastChecked"],
                    "created_at": proxy["created_at"],
                    "updated_at": proxy["updated_at"],
                    "working_percent": proxy["workingPercent"],
                    "uptime_try_count": proxy["upTimeTryCount"],
                    "uptime_success_count": proxy["upTimeSuccessCount"],
                    "uptime": proxy["upTime"],
                    "speed": proxy["speed"],
                    "response_time": proxy["responseTime"],
                    "region": proxy["region"],
                    "anonymity_level": proxy["anonymityLevel"],
                    "protocols": proxy["protocols"],
                    "org": proxy["org"],
                    "latency": proxy["latency"],
                    "isp": proxy["isp"],
                    "google": proxy["google"],
                    "city": proxy["city"],
                    "asn": proxy["asn"],
                }

                if self.validate_proxy(proxy_data):
                    results.append(proxy_data)
                    self.get_or_update(proxy_data)

            return Response(results, status=200)
        else:
            return Response({"detail": "Failed to retrieve proxy data."}, status=500)

    def get_proxy_json(self, limit=500):
        url = f"https://proxylist.geonode.com/api/proxy-list?limit={limit}&country=US&page=1&sort_by=lastChecked&sort_type=desc"

        try:
            response = requests.get(url)
            response.raise_for_status()

            json_data = response.json()
            if json_data and json_data.get("data"):
                return json_data["data"]
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_or_update(self, proxy_data):
        try:
            instance, created = Proxy.objects.update_or_create(
                ip=proxy_data["ip"], port=proxy_data["port"], defaults=proxy_data
            )

            serializer = self.get_serializer(instance)
            status_code = 201 if created else 200
            return Response(serializer.data, status=status_code)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
