from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reviews = models.IntegerField()
    images = models.JSONField()
    availability = models.BooleanField()
    variants = models.JSONField()