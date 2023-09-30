from django.db import models
from users.models import UserAccount as User
from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)  # Optional link related to the notification

    def __str__(self):
        return self.message

class NotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_email = models.BooleanField(default=False)
    receive_push = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Notification Settings"
