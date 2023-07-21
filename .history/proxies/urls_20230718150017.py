from django.urls import path
from .views import ProxyViewSet

urlpatterns = [
    path(
        "proxy/list/all/",
        ProxyViewSet.as_view(actions={"get": "list-all"}),
        name="proxy-list-all",
    ),
    path(
        "proxy/list/<int:limit>/",
        ProxyViewSet.as_view(actions={"get": "list"}),
        name="proxy-list",
    ),
    path(
        "proxy/add/<int:limit>/",
        ProxyViewSet.as_view(actions={"post": "populate"}),
        name="proxy-create",
    ),
]
