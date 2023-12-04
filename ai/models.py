from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import UserAccount as User
# Create your models here.

# name andorder mixins


class NameAndOrderable(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['updated_at', 'name']

    def __str__(self):
        return self.name


class AssistantModel(NameAndOrderable, models.Model):
    description = models.CharField(max_length=500, blank=True, null=True)
    model_object = models.TextField()
    model_created = models.TextField()
    model_owned_by = models.TextField()

class Assistant(NameAndOrderable, models.Model):
    primary_assistant = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    system_instructions = models.TextField(null=True, blank=True)
    model = models.ForeignKey(
        AssistantModel, related_name="assistant_models", on_delete=models.SET_NULL, blank=True, null=True, error_messages={'null': 'Please select a model', 'blank': 'Please select a model'})


class ChatMessage(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Create ContentType and object_id fields to store the user reference
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')

class ChatRoom(NameAndOrderable, models.Model):
    is_active = models.BooleanField(default=True, blank=True, null=True)
    description = models.CharField(max_length=50)
    assistant = models.ForeignKey(
        Assistant, related_name="assistants", on_delete=models.SET_NULL, blank=True, null=True, error_messages={'null': 'Please select an assistant', 'blank': 'Please select an assistant'})
    user = models.ForeignKey(
        User, related_name="users", on_delete=models.SET_NULL, blank=True, null=True, error_messages={'null': 'Please select a user', 'blank': 'Please select a user'})
    messages = models.ManyToManyField(ChatMessage, related_name="chat_messages", blank=True, null=True)
        
    def __str__(self):
        return self.name

    
