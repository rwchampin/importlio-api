from djoser.serializers import UserSerializer
from .models import UserAccount  # Import your custom user model
from rest_framework import serializers

class CustomCurrentUserSerializer(UserSerializer):
    class Meta:
        model = UserAccount
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'address',
            'city',
            'state',
            'is_active',
            'is_staff',
            'is_superuser',
            'avatar',
        )

