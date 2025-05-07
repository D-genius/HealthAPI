from celery import shared_task
from .models import Appointment
from doctors.models import Availability
from patients.models import Patient
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db import transaction
import datetime  # Added import for datetime

@shared_task
def schedule_appointment(id, doctor_id, scheduled_datetime_str):
    patient = Patient.objects.get(id=id)

    scheduled_datetime = parse_datetime(scheduled_datetime_str)
    if timezone.is_naive(scheduled_datetime):
        scheduled_datetime = timezone.make_aware(scheduled_datetime, datetime.timezone.utc)

    # Check availability
    available = Availability.objects.filter(
        doctor_id=doctor_id,
        start_datetime__lte=scheduled_datetime,
        end_datetime__gte=scheduled_datetime,
        is_available=True
    ).exists()

    if not available:
        return ValueError(f"Doctor {doctor_id} not available at {scheduled_datetime}")

    # Check conflicts
    buffer = timezone.timedelta(minutes=15)
    conflict = Appointment.objects.filter(
        doctor_id=doctor_id,
        scheduled_datetime__range=(
            scheduled_datetime - buffer,
            scheduled_datetime + buffer
        )
    ).exists()
    if conflict:
        raise ValueError(f"Appointment slot at {scheduled_datetime} already booked")

    # Create appointment
    appointment = Appointment.objects.create(
        patient=patient,
        doctor_id=doctor_id,
        scheduled_datetime=scheduled_datetime,
        status='booked'
    )
    return appointment.id