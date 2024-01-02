from django.db import models

# Create your models here.
class SocialAccount(models.Model):
    platform = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.platform + ' - ' + self.username