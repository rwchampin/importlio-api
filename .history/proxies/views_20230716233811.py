from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Proxy
from .serializers import ProxySerializer
from proxybroker import Broker


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
