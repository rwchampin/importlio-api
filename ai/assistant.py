from openai import OpenAI
import tiktoken
from .models import Assistant, ChatRoom, ChatMessage
# class for openai manager that handles the init, and custom functions


class AssistantManager:
    # init function
    def __init__(self):
        self.client = OpenAI()
        self.model_options = self.client.models.list()
        self.assistant = Assistant()

    # function to get the model options
    def get_model_options(self):
        print(self.model_options)
        return self.model_options
    
    # return assistants
    def get_assistants(self):
        return Assistant.objects.all()


class Assistant:
    # init function
    def __init__(self):
        self.model = None
        self.chatroom = ChatRoom()

    # function to set the model

    def set_model(self, model):
        self.model = model
