from rest_framework import serializers
from .models import Post, UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = UserAccount
        fields = ('avatar',)  # Include other fields if needed


class PostSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer()

    class Meta:
        model = Post
        fields = '__all__'
