# from djoser.serializers import UserSerializer
from .models import UserAccount  # Import your custom user model
from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
class UserAccountSerializer(UserSerializer):
    
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'avatar')
        # lookup_field = 'email'
 

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.save()
    #     return instance
    
    # def create(self, validated_data):
    #     user = UserAccount.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #     return user
 