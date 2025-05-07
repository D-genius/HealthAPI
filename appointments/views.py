from rest_framework import viewsets, status, permissions
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
        user = self.request.user
        if user.user_type == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.user_type != 'patient':
            raise PermissionDenied("Only patients can book appointments.")
        # Trigger task synchronously
        task = schedule_appointment.apply(
            args=(
                request.user.id,  # user_id
                request.data.get('doctor'),  # doctor_id
                request.data.get('scheduled_datetime'),  # scheduled_datetime_str
                # request.data.get('follow_up_datetime')  # follow_up_datetime_str
            ),
            throw=True  # Run synchronously and raise any errors
        )

        try:
            result = task.get()  # Get the result from the task
            if isinstance(result, int):  # Check if the result is an integer (appointment ID)
                appointment_id = result
                # Fetch the created appointment to serialize it
                appointment = Appointment.objects.get(id=appointment_id)
                serializer = self.get_serializer(appointment)
                # return Response({'task_id': task.id}, status=status.HTTP_201_CREATED)
                return Response(serializer.data, status=status.HTTP_200_OK)  # Return 200 OK with appointment data

            else:
                return Response({"error": str(result)}, status=status.HTTP_400_BAD_REQUEST)  # Handle unexpected result
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  # Return 400 if doctor is not available