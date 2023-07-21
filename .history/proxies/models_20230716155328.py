from django.db import models

# Create your models here.
from django.db import models


class Proxy(models.Model):
    working_percent = models.FloatField()
    uptime_try_count = models.PositiveIntegerField()
    uptime_success_count = models.PositiveIntegerField()
    uptime = models.FloatField()
    updated_at = models.DateTimeField()
    speed = models.FloatField()
    response_time = models.FloatField()
    region = models.CharField(max_length=100)
    anonymity_level = models.CharField(max_length=100)
    protocols = models.CharField(max_length=100)
    port = models.PositiveIntegerField()
    org = models.CharField(max_length=100)
    latency = models.FloatField()
    last_checked = models.DateTimeField()
    isp = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    google = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    asn = models.CharField(max_length=100)

    def __str__(self):
        return self.ip
