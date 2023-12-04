from django.urls import path, re_path
from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
    UserAccountViewSet,
)
from rest_framework import routers
from django.conf.urls import include



urlpatterns = [
    
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    # path('send-admin-email/', send_admin_notification.as_view()),
    # path('auth/users-email/<str:email>/', UserAccountViewSet.as_view({'get': 'retrieve'})),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
]