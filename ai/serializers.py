from rest_framework import serializers
 
 
from .models import Assistant, ChatRoom, ChatMessage
 

class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = '__all__'
        
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = ChatRoom
        fields = '__all__'
        
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = ChatMessage
        fields = '__all__'
   