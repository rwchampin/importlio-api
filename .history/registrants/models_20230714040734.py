from django.db import models

# Create your models here.
class Registrant(models.Model):
    email = models.EmailField()

    