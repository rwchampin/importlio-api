from django.db import models

    
class Product(models.Model):
    asin = models.CharField(max_length=255, null=True, blank=True)
    title = models.TextField(default='', null=True, blank=True)
    image = models.TextField(default='', null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    reviews = models.CharField(max_length=255, null=True, blank=True)
    rating = models.CharField(max_length=255, null=True, blank=True)
    product_url = models.TextField(default='', null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class SearchURL(models.Model):
    url = models.TextField(default='', null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    
    def __str__(self):
        return self.url
    
    
class ProductList(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    
    def __str__(self):
        return self.name