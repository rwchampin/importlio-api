from django.db import models

# Create your models here.
class Registrant(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    # created = models.DateTimeField(auto_now_add=True)
    # def create(self, validated_data):

        
    #     email = validated_data.pop('email')
    #     email = email.lower()

    #     first_name 
    #     # generate uid and token for emauk 

    def __str__(self):
        return self.email