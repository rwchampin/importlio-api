
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Registrant
from .serializers import RegistrantSerializer
from .utils import send_registration_email


class RegistrantViewSet(viewsets.ModelViewSet):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    lookup_field = 'email'

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Custom email validation
        if not is_valid_email(email):
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Send registration email
        send_registration_email(email)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
