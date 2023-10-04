from django.urls import path
from .views import RegistrantListCreateView, RegistrantDetailView, RegistrantEmailDetailView


urlpatterns = [
    path('registrants/', RegistrantListCreateView.as_view(), name='registrant-list-create'),
    path('registrants/<int:pk>/', RegistrantDetailView.as_view(), name='registrant-detail'),
    path('registrants/<str:email>/', RegistrantEmailDetailView.as_view(), name='registrant-email-detail'),
]
