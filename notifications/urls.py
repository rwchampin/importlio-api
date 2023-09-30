from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet)
router.register(r'notification-settings', views.NotificationSettingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
