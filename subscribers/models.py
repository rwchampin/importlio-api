from django.db import models

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True, error_messages={'blank': 'Email is required', 'unique': 'Email already exists'})
    
    def __str__(self):
        return self.email