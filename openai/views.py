from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny  # Import AllowAny permission class

from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from rest_framework import viewsets
 
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]