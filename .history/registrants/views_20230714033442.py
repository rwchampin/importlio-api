from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Registrant
from .serializers import RegistrantSerializer


class RegistrantViewSet(viewsets.ModelViewSet):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer


class RegisterViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegistrantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
