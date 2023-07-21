from django.db import models

# Create your models here.
from django.db import models


class Proxy(models.Model):
    working_percent = models.FloatField(null=True)
    uptime_try_count = models.PositiveIntegerField()
    uptime_success_count = models.PositiveIntegerField()
    uptime = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    speed = models.FloatField()
    response_time = models.FloatField()
    region = models.CharField(max_length=100, null=True)
    anonymity_level = models.CharField(max_length=100, null=True)
    protocols = models.CharField(max_length=100)
    port = models.PositiveIntegerField()
    org = models.CharField(max_length=100, null=True, blank=True)
    latency = models.FloatField()
    last_checked = models.DateTimeField(auto_now=True)
    isp = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    google = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    asn = models.CharField(max_length=100)

    def __str__(self):
        return self.ip
