from django.urls import path
from .views import RoomCreateView, RoomRetrieveView, RoomUpdateView, RoomDeleteView

urlpatterns = [
    path('room/', RoomCreateView.as_view(), name='room-create'),
    path('room/<int:id>/', RoomRetrieveView.as_view(), name='room-retrieve'),
    path('room/<int:id>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('room/<int:id>/delete/', RoomDeleteView.as_view(), name='room-delete'),
]
