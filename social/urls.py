from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.SocialAccountViewSet)


urlpatterns = [
    path('social/add-followers/', views.follow, name='follow'),
    path('social/message-users/', views.message_users, name='message-users'),
    path('social/', include(router.urls)),
]
