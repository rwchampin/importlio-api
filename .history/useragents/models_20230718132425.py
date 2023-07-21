from django.db import models


# Create your models here.
class UserAgent(models.Model):
    useragent = models.CharField(max_length=255, blank=True, null=True)
    last_used = models.DateTimeField(blank=True, null=True)
	sucess_last_used = models.DateTimeField(blank=True, null=True)
	product = models.CharField(max_length=255, blank=True, null=True)
	web_browser = models.CharField(max_length=255, blank=True, null=True)