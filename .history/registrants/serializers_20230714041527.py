from rest_framework import serializers, viewsets, status
from .models import Registrant
from rest_framework.response import Response
from rest_framework.decorators import action

class RegistrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrant
        fields = ['email']
        read_only_fields = ['email']  # Set 'email' field as read-only


class RegistrantViewSet(viewsets.GenericViewSet):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegistrantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
