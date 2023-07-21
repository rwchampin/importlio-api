from .views import ProxyViewset
from django.urls import path

urlpatterns = [
    path('proxies/', ProxyViewset.as_view({'get': 'list'}), name='proxy-list'),
    path('proxies/populate/', ProxyViewset.as_view({'post': 'populate'}), name='proxy-populate'),
    path('proxies/<int:pk>/', ProxyViewset.as_view({'get': 'retrieve'}), name='proxy-detail'),
]