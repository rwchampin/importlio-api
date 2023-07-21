from rest_framework import serializers
from .models import Proxy

class ProxySerializer(serializers.ModelSerializer):
    class meta:
        model = Proxy
        fields = '__all__'