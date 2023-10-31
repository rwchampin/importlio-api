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
    search_url = models.URLField()
    img = models.ImageField(upload_to='images/', null=True, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)