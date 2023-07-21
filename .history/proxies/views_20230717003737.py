from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Proxy
from .serializers import ProxySerializer
import requests
from rest_framework.exceptions import ValidationError


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["get"])
    def get_queryset(self):
        queryset = Proxy.objects.all()
        limit = self.request.query_params.get("limit", None)
        if limit is not None:
            queryset = queryset[: int(limit)]
        return queryset

    def get_proxy_json(self, limit=500):
        url = (
            "https://proxylist.geonode.com/api/proxy-list?limit="
            + str(limit)
            + "&page=1&sort_by=lastChecked&sort_type=desc"
        )

        try:
            json = requests.get(url).json()
            if json and json["data"]:
                return json["data"]
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def save_proxy(self, proxy):
        try:
            # check if proxy exists
            exists = Proxy.objects.get(ip=proxy["ip"], port=proxy["port"])

            if exists:
                # if proxy exists, update the proxy
                serializer = self.get_serializer(exists, data=proxy)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            else:
                # if proxy does not exist, create the proxy
                serializer = self.get_serializer(data=proxy)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # return json object that was saved
                return Response(serializer.data, status=201)
        except Exception as e:
            print(e)
            print(
                "Error saving proxy, check the netork response from the api were getting proxies from"
            )
            return Response(serializer.data, status=500)

    @action(detail=False, methods=["post"])
    def populate(self, request, *args, **kwargs):
        # Get the limit from the URL
        limit = kwargs.get("limit", None)
        limit = int(limit)

        if not limit:
            raise ValidationError("Limit must be provided")

        proxy_json = self.get_proxy_json(limit=limit)

        if proxy_json is not None:
            results = []
            # Save proxies to a text file

            for proxy in proxy_json:
                proxy = {
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
                    "anonimity_level": proxy["anonymityLevel"],
                    "protocols": proxy["protocols"],
                    "org": proxy["org"],
                    "latency": proxy["latency"],
                    "last_checked": proxy["lastChecked"],
                    "isp": proxy["isp"],
                    "google": proxy["google"],
                    "city": proxy["city"],
                    "asn": proxy["asn"],
                    "country": proxy["country"],
                }

            self.save_proxy(proxy)

            # return json object that was saved
            return Response(serializer.data, status=201)
