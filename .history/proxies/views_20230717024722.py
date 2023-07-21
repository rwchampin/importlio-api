from rest_framework.decorators import action
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .models import Proxy
from .serializers import ProxySerializer
import requests
from rest_framework.exceptions import ValidationError

judge = "https://httpbin.org/ip"


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    authentication_classes = []
    permission_classes = []

    def validate(self, proxy):
        try:
            response = requests.get(judge, proxies=proxy, timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

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

                if self.validate(proxy_data):
                    results.append(proxy_data)
                    self.get_or_update(proxy_data)

            return Response(results, status=200)

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

    def create_proxy_header(self, proxy):
        header = {
            "http": "http://" + proxy.ip + ":" + str(proxy.port),
            "https": "https://" + proxy.ip + ":" + str(proxy.port),
        }

        return {header: header, proxy: proxy}

    def validate(self, proxy):
        try:
            response = requests.get(judge, proxies=proxy, timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


[
    {
        "ip": "75.119.201.151",
        "port": "15745",
        "country": "US",
        "last_checked": 1689576351,
        "created_at": "2022-08-30T13:16:35.970Z",
        "updated_at": "2023-07-17T06:45:51.249Z",
        "working_percent": null,
        "uptime_try_count": 2930,
        "uptime_success_count": 2929,
        "uptime": 99.96587030716724,
        "speed": 1,
        "response_time": 2688,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks5"],
        "org": "New Dream Network, LLC",
        "latency": 191.428,
        "isp": "New Dream Network, LLC",
        "google": false,
        "city": "Brea",
        "asn": "AS26347",
    },
    {
        "ip": "80.191.169.66",
        "port": "4145",
        "country": "IR",
        "last_checked": 1689576351,
        "created_at": "2022-09-05T10:18:57.055Z",
        "updated_at": "2023-07-17T06:45:51.241Z",
        "working_percent": null,
        "uptime_try_count": 2895,
        "uptime_success_count": 2606,
        "uptime": 90.01727115716753,
        "speed": 1,
        "response_time": 4608,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks4"],
        "org": "Azad University of Anar",
        "latency": 110.161,
        "isp": "Information Technology Company",
        "google": false,
        "city": "Anār",
        "asn": "AS58224",
    },
    {
        "ip": "161.35.229.155",
        "port": "61658",
        "country": "US",
        "last_checked": 1689576351,
        "created_at": "2022-09-09T22:19:57.594Z",
        "updated_at": "2023-07-17T06:45:51.441Z",
        "working_percent": null,
        "uptime_try_count": 2906,
        "uptime_success_count": 2905,
        "uptime": 99.96558843771507,
        "speed": 1,
        "response_time": 4798,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks5"],
        "org": "DigitalOcean, LLC",
        "latency": 199.395,
        "isp": "DigitalOcean, LLC",
        "google": false,
        "city": "Santa Clara",
        "asn": "AS14061",
    },
    {
        "ip": "177.38.5.19",
        "port": "4153",
        "country": "BR",
        "last_checked": 1689576351,
        "created_at": "2022-08-30T16:15:17.293Z",
        "updated_at": "2023-07-17T06:45:51.247Z",
        "working_percent": null,
        "uptime_try_count": 2931,
        "uptime_success_count": 2843,
        "uptime": 96.99761173660868,
        "speed": 1,
        "response_time": 4897,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks4"],
        "org": "FÁBIO MENDES DIAS LTDA ME",
        "latency": 296.033,
        "isp": "FÔBIO MENDES DIAS LTDA ME",
        "google": false,
        "city": "Poco Fundo",
        "asn": "AS52964",
    },
    {
        "ip": "103.12.246.65",
        "port": "4145",
        "country": "IN",
        "last_checked": 1689576351,
        "created_at": "2022-08-26T19:00:08.262Z",
        "updated_at": "2023-07-17T06:45:51.242Z",
        "working_percent": null,
        "uptime_try_count": 2947,
        "uptime_success_count": 2926,
        "uptime": 99.2874109263658,
        "speed": 1,
        "response_time": 826,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks4"],
        "org": "Instant Cable Network PVT LTD",
        "latency": 173.27,
        "isp": "Instant Cable Network PVT LTD",
        "google": false,
        "city": "Gurugram",
        "asn": "AS134941",
    },
    {
        "ip": "37.221.146.138",
        "port": "1080",
        "country": "UA",
        "last_checked": 1689576351,
        "created_at": "2022-09-09T04:04:12.744Z",
        "updated_at": "2023-07-17T06:45:51.246Z",
        "working_percent": null,
        "uptime_try_count": 2912,
        "uptime_success_count": 2512,
        "uptime": 86.26373626373626,
        "speed": 1,
        "response_time": 4392,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks5"],
        "org": "Radio Service Ltd",
        "latency": 83.358,
        "isp": "Radio Service Ltd.",
        "google": false,
        "city": "Dolyna",
        "asn": "AS3255",
    },
    {
        "ip": "180.183.225.197",
        "port": "4145",
        "country": "TH",
        "last_checked": 1689576351,
        "created_at": "2022-08-30T13:35:21.882Z",
        "updated_at": "2023-07-17T06:45:51.244Z",
        "working_percent": null,
        "uptime_try_count": 2918,
        "uptime_success_count": 2557,
        "uptime": 87.62851267991775,
        "speed": 1,
        "response_time": 4902,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks4"],
        "org": "Triple T Broadband Public Company Limited",
        "latency": 185.352,
        "isp": "Triple T Broadband Public Company Limited",
        "google": false,
        "city": "Chiang Mai",
        "asn": "AS45629",
    },
    {
        "ip": "185.20.26.41",
        "port": "43051",
        "country": "IQ",
        "last_checked": 1689576346,
        "created_at": "2022-08-22T13:11:48.687Z",
        "updated_at": "2023-07-17T06:45:46.836Z",
        "working_percent": null,
        "uptime_try_count": 2943,
        "uptime_success_count": 2747,
        "uptime": 93.34012911994563,
        "speed": 1,
        "response_time": 2092,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks4"],
        "org": "SCOPSKY Service",
        "latency": 113.446,
        "isp": "Data Net Company for Communications Limited",
        "google": false,
        "city": "Baghdad",
        "asn": "AS60815",
    },
    {
        "ip": "185.139.69.118",
        "port": "20997",
        "country": "RU",
        "last_checked": 1689576346,
        "created_at": "2022-08-30T16:06:34.354Z",
        "updated_at": "2023-07-17T06:45:46.835Z",
        "working_percent": null,
        "uptime_try_count": 2928,
        "uptime_success_count": 2429,
        "uptime": 82.95765027322405,
        "speed": 1,
        "response_time": 5300,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks5"],
        "org": "Firstbyte Hosting",
        "latency": 92.825,
        "isp": "First Server Limited",
        "google": false,
        "city": "Moscow",
        "asn": "AS204997",
    },
    {
        "ip": "180.211.158.90",
        "port": "5678",
        "country": "BD",
        "last_checked": 1689576346,
        "created_at": "2022-08-23T01:15:04.932Z",
        "updated_at": "2023-07-17T06:45:46.842Z",
        "working_percent": null,
        "uptime_try_count": 2945,
        "uptime_success_count": 2653,
        "uptime": 90.0848896434635,
        "speed": 1,
        "response_time": 4796,
        "region": null,
        "anonymity_level": "elite",
        "protocols": ["socks4"],
        "org": "",
        "latency": 187.854,
        "isp": "Bangladesh Telecommunications Company Ltd.",
        "google": false,
        "city": "Azimpur",
        "asn": "AS45588",
    },
]
