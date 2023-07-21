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
            + limit
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

        if not limit:
            raise ValidationError("Limit must be provided")

        limit = int(limit)

        broker = Broker()
        broker.find(
            types=[protocols],
            limit=limit,
            countries=[countries],
            anonymity_levels=[anonymity_levels],
        )
        results = []
        while True:
            proxy = broker.get()
            if proxy is None:
                break
            results.append(proxy)

        # Save proxies to a text file
        with open("out.txt", "w") as file:
            for proxy in results:
                file.write(str(proxy) + "\n")
        import pdb

        pdb.set_trace()
        serializer = self.get_serializer(data=results, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
