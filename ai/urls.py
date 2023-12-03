from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assistants', views.AssistantViewSet)
router.register(r'chat-rooms', views.ChatRoomViewSet)
router.register(r'chat-messages', views.ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
