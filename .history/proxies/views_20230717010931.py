from rest_framework.decorators import action
from rest_framework import viewsets, serializers
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

    def get_or_update(self, proxy_data):
        try:
            instance = Proxy.objects.filter(
                ip=proxy_data["ip"], port=proxy_data["port"]
            ).first()
            if instance:
                serializer = self.get_serializer(
                    instance, data=proxy_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    serializer.data, status=200
                )  # Success, updated the instance
            else:
                serializer = self.get_serializer(data=proxy_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    serializer.data, status=201
                )  # Success, created a new instance
        except serializers.ValidationError as e:
            return Response(e.detail, status=400)  # Bad request, validation error
        except Exception as e:
            return Response(str(e), status=500)  # Server error

    @action(detail=False, methods=["post"])
    def populate(self, request, *args, **kwargs):
        limit = kwargs.get("limit", None)
        limit = int(limit)

        if not limit:
            raise ValidationError("Limit must be provided")

        proxy_json = self.get_proxy_json(limit=limit)

        if proxy_json is not None:
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

                results.append(proxy_data)
                self.get_or_update(proxy_data)

            return Response(results, status=200)
