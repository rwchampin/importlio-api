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

class UserAccountCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'avatar')
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'blank': 'Email is required',
                    'unique': 'Email already exists',
                }
            },
        }
        
    def validate_email(self, value):
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        
    def validate(self, data):
        if data['password'] == '' or data['password'] == None:
            data['password'] = 'password'
            data['password_confirmation'] = 'password'
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user