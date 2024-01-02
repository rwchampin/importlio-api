# from djoser.serializers import UserSerializer
from .models import SocialAccount
from djoser.serializers import UserSerializer

class SocialAccountSerializer(UserSerializer):
    
    class Meta:
        model = SocialAccount
        fields = ('id', 'platform', 'username', 'password')
        # lookup_field = 'email'
 