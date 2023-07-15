from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Registrant
from .serializers import RegistrantSerializer


class RegistrantViewSet(viewsets.ModelViewSet):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = []
    
class RegisterViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        email = request.data.get('email', '')
        try:
            validate_email(email)
            serializer = RegistrantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

