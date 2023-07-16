from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Registrant

class RegistrantSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")

    class Meta:
        model = Registrant
        fields = ['id', 'email']
