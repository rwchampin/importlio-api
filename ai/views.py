from django.shortcuts import render
from .serializers import AssistantSerializer, ChatRoomSerializer, ChatMessageSerializer
from .models import Assistant, ChatRoom, ChatMessage
from rest_framework import viewsets
# Create your views here.

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer