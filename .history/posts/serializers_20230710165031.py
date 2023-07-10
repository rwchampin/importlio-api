from rest_framework import serializers
from users.models import UserAccount
from .models import Post

class UserAccountSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = UserAccount
        fields = ('avatar','first_name, 'last_name')  # Include other fields if needed


class PostSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer()

    class Meta:
        model = Post
        fields = '__all__'
