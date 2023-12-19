# from djoser.serializers import UserSerializer
from .models import UserAccount, ContactMessage
from djoser.serializers import UserSerializer
class UserAccountSerializer(UserSerializer):
    
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'avatar', 'account_type', 'amazon_associate_id', 'phone', 'address', 'city', 'state', 'country', 'tz', 'region')
        # lookup_field = 'email'
 
class ContactMessageSerializer(UserSerializer):
        
        class Meta:
            model = ContactMessage
            fields = ('id', 'name', 'email', 'message', 'date')