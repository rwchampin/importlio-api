from django.shortcuts import render
from .serializers import AssistantSerializer, ChatRoomSerializer, ChatMessageSerializer, AssistantModelSerializer
from .models import Assistant, ChatRoom, ChatMessage, AssistantModel
from rest_framework import viewsets, generics, status, filters
from .assistant import AssistantManager, Assistant as AssistantAI
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from rest_framework.response import Response


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
    

@api_view(['POST'])
def audio(request):
    audio = request.FILES.get('audio', None)

    if audio is None:
        print('Audio not specified')
        # return Response({'message': 'Audio not specified'}, status=status.HTTP_400_BAD_REQUEST)
    
    if audio:
        # turn audio file to bytes
        audio = audio.read()
        manager = AssistantAI()
        transcript = manager.process_audio(audio)

        return Response({'transcript': transcript}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    # return Response({'message': 'Processed'}, status=status.HTTP_200_OK)