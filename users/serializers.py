from djoser.serializers import UserSerializer
from .models import UserAccount  # Import your custom user model


class UserAccountSerializer(UserSerializer):
    
    class Meta:
        model = UserAccount
        fields = '__all__'

