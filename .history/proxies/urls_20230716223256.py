from .views import ProxyViewset, ProxyPopulateView
from django.urls import path

urlpatterns = [
    path("proxies/", ProxyViewset.as_view({"get": "list"}), name="proxy-list"),
    path(
        "proxy-population/<int:limit>/",
        ProxyPopulationView.as_view(),
        name="proxy-population",
    ),
    path(
        "proxies/<int:pk>/",
        ProxyViewset.as_view({"get": "retrieve"}),
        name="proxy-detail",
    ),
]
