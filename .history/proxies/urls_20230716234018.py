from django.urls import path
from .views import ProxyViewSet

urlpatterns = [
    path("proxy/all/", ProxyViewSet.as_view({"get": "list"}), name="proxy-list"),
    path(
        "proxy/add/<int:limit>/",
        ProxyViewSet.as_view({"post": "populate"}),
        name="proxy-create",
    ),
]
