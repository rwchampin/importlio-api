from rest_framework import serializers
from .models import Proxy


class ProxySerializer(serializers.ModelSerializer):
    protocols = serializers.ListField(
        child=serializers.CharField(allow_blank=True, allow_null=True),
        allow_empty=True,
    )

    class Meta:
        model = Proxy
        fields = "__all__"
