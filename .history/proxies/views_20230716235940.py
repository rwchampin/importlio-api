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
            with open("out.txt", "w") as file:
                for proxy in proxy_json:
                    file.write(str(proxy) + "\n")

            serializer = self.get_serializer(data=results, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=201)
