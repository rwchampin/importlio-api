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
    
    def get_proxy_json():
        url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'
        try:
            requests.get(url).json()
        

    @action(detail=False, methods=["post"])
    def populate(self, request, *args, **kwargs):
        protocols = request.data.get("protocols")
        limit = request.parser_context["kwargs"].get("limit")
        countries = request.data.get("countries")
        anonymity_levels = request.data.get("anonymity_levels")

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
