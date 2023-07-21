from django.db import models

# Create your models here.
class Registrant(models.Model):
    email = models.EmailField()

    def create(self, validated_data):

        email = validated_data.pop('email')
        email = email.lower()

        # generate uid and token for emauk 

    def __str__(self):
        return self.email