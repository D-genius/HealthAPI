from celery import shared_task
from .models import Appointment
from doctors.models import Availability
from patients.models import Patient
from django.utils import timezone
from django.db import transaction

@shared_task
def schedule_appointment(user_id, doctor_id, scheduled_datetime):
    patient = Patient.objects.get(user_id=user_id)
    scheduled_datetime = timezone.make_aware(timezone.datetime.fromisoformat(scheduled_datetime))
    # Check availability
    available = Availability.objects.filter(
        doctor_id=doctor_id,
        start_datetime__lte=scheduled_datetime,
        end_datetime__gte=scheduled_datetime,
        is_available=True
    ).exists()

    if not available:
        return ValueError("Doctor not available at this time.")

    # Check conflicts
    conflict = Appointment.objects.filter(
        doctor_id=doctor_id,
        scheduled_datetime=scheduled_datetime
    ).exists()
    if conflict:
        return ValueError("Appointment slot already booked.")

    # Create appointment
    appointment = Appointment.objects.create(
        patient=patient,
        doctor_id=doctor_id,
        scheduled_datetime=scheduled_datetime,
        status='booked'
    )
    return appointment.id