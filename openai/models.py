from django.db import models
from users.models import UserAccount as User

bots = (
    ("gpt3.5-turbo", "GPT3.5 Turbo"),
    ("gpt3.5", "GPT3.5"),
    ("gpt4", "GPT4"),
)

authors = (
    ("user", "User"),
    ("bot", "Bot")
)
class Room(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    bot_type = models.CharField(max_length=255, choices=bots, default=bots[0][0])    
    
    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"
