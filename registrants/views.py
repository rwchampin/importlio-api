from rest_framework import generics
from .models import Registrant
from .serializers import RegistrantSerializer
from .utils import send_subscriber_signup_alert_email
class RegistrantListCreateView(generics.ListCreateAPIView):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    authentication_classes = []
    permission_classes = []
    
    # send email to admin on create
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     send_subscriber_signup_alert_email(instance.email)

class RegistrantDetailView(generics.RetrieveAPIView):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    authentication_classes = []
    permission_classes = []
    
class RegistrantEmailDetailView(generics.RetrieveAPIView):
    queryset = Registrant.objects.all()
    serializer_class = RegistrantSerializer
    authentication_classes = []
    permission_classes = []
    lookup_field = 'email'
    
    
 