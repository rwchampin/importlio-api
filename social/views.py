from django.shortcuts import render
from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .manager import Manager as SocialManager
from users.manager import Manager as UserManager
from .models import SocialAccount
from .serializers import SocialAccountSerializer
# Create your views here.

class SocialAccountViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = SocialAccountSerializer
    
@api_view(['POST'])
def follow(request):

    platform = request.data.get('platform', None)
    action = request.data.get('action', None)
    platform_username = request.data.get('platform_username', None)
    platform_password = request.data.get('platform_password', None)
    importlio_username = request.data.get('importlio_username', None)
    importlio_password = request.data.get('importlio_password', None)

    
    try:
        manager = SocialManager()
        if manager.login(platform_username, platform_password):
            manager.get_followers('https://twitter.com/thefoothunter1/followers')
            if action == 'add followers':
                manager.get_followers('https://twitter.com/X')
            # elif action == 'unfollow':
            #     manager.unfollow()
            else:
                return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print('Error: ', e)
        return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
   
    return Response({'message': 'Followed'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def message_users(request):
    tag = '#shopify'
    
    mn = Manager()
    mn.send_messages(tag)