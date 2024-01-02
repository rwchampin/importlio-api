from django.shortcuts import render
from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .manager import Manager
from users.manager import Manager as UserManager
from .models import SocialAccount
from .serializers import SocialAccountSerializer
# Create your views here.

class SocialAccountViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = SocialAccountSerializer
    
@api_view(['POST'])
def follow(request):
    email = request.data.get('email', None)
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    platform = request.data.get('platform', None)
    
    if platform is None:
        return Response({'message': 'Platform not specified'}, status=status.HTTP_400_BAD_REQUEST)
    
    if email is None:
        return Response({'message': 'Email not specified'}, status=status.HTTP_400_BAD_REQUEST)
    
    if username is None or password is None:
        return Response({'message': 'Username or password not specified'}, status=status.HTTP_400_BAD_REQUEST)
    
    if platform and username and password and email:
        if UserManager.get(email) is None:
            return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        manager = Manager(username, password, platform)
        manager.follow()
    else:
        return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
   
    return Response({'message': 'Followed'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def message_users(request):
    tag = '#shopify'
    
    mn = Manager()
    mn.send_messages(tag)