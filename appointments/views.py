from rest_framework import viewsets, status ,permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Appointment
from users.serializers import AppointmentSerializer
from .tasks import schedule_appointment
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['write']

    def get_queryset(self):
        user= self.request.user
        if user.user_type == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.user_type != 'patient':
            raise PermissionDenied("Only patients can book appointments.")
        #Trigger async task
        task = schedule_appointment.delay(
            request.data.get('doctor'),
            request.data.get('scheduled_appointment'),
            request.user.id
        )
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)