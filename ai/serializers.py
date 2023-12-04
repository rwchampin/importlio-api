from rest_framework import serializers
 
 
from .models import Assistant, ChatRoom, ChatMessage, AssistantModel
 

class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = '__all__'
        
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = ChatRoom
        fields = '__all__'
        
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = ChatMessage
        fields = '__all__'
   
class AssistantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantModel
        fields = '__all__'