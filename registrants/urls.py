from django.urls import path
from .views import RegistrantListCreateView, RegistrantDetailView


urlpatterns = [
    path('registrants/create/', RegistrantListCreateView.as_view(), name='registrant-list-create'),
    path('registrants/<int:pk>/', RegistrantDetailView.as_view(), name='registrant-detail'),
]
