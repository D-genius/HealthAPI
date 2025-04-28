from rest_framework import viewsets, permissions
from .models import Patient
from users.serializers import PatientSerializer
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated,TokenHasScope]
    required_scopes = ['write']