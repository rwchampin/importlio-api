from django.shortcuts import render
from .serializers import AssistantSerializer, ChatRoomSerializer, ChatMessageSerializer, AssistantModelSerializer
from .models import Assistant, ChatRoom, ChatMessage, AssistantModel
from rest_framework import viewsets
from .assistant import AssistantManager
# Create your views here.

class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    
class AssistantModelViewSet(viewsets.ModelViewSet):
    queryset = AssistantModel.objects.all()
    serializer_class = AssistantModelSerializer
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    
