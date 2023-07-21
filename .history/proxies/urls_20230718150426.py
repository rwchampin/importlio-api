from django.urls import path, include
from rest_framework import routers
from .views import ProxyViewSet

urlpatterns = [
    path(
        "proxy/list/all/",
        ProxyViewSet.as_view(actions={"get": "list_all"}),
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


router = routers.DefaultRouter()
router.register(r"proxy", ProxyViewSet)

urlpatterns = [
    # Your other URL patterns
    path("api/", include(router.urls)),
]
