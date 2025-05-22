from rest_framework import viewsets, permissions
from .models import Doctor, Availability
from users.serializers import DoctorSerializer, AvailabilitySerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['write']

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated,TokenHasScope]
    required_scopes = ['read']

    def get_queryset(self):
        return Availability.objects.filter(doctor__user=self.request.user)