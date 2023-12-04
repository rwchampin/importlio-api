from django.contrib import admin
from .models import Assistant, ChatRoom, ChatMessage, AssistantModel
# Register your models here.

admin.site.register(Assistant)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(AssistantModel)