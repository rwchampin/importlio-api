from django.db import models

    
class Product(models.Model):
    title = models.TextField(default='', null=True, blank=True)
    image = models.TextField(default='', null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    rating = models.CharField(max_length=255, null=True, blank=True)
    
class SearchURL(models.Model):
    url = models.URLField(unique=True)
    product = models.ManyToManyField(Product, related_name='search_url', blank=True, null=True)