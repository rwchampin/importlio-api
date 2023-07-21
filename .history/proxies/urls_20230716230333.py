from django.urls import path
from .views import ProxyListView, ProxyCreateView

urlpatterns = [
    path("proxy/all/", ProxyListView.as_view(), name="proxy-list"),
    path("proxy/add/<int:limit>/", ProxyCreateView.as_view(), name="proxy-create"),
]
