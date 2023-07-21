from django.urls import path, include
from rest_framework import routers
from .views import ProxyViewSet

router = routers.DefaultRouter()
router.register(r"proxy", ProxyViewSet)

urlpatterns = [
    # Your other URL patterns
    path("api/", include(router.urls)),
]
