from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    class Status(models.TextChoices):
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_datetime = models.DateTimeField()
    follow_up_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BOOKED)

    def __str__(self):
        return f"{self.patient} Appointment with {self.doctor} at {self.scheduled_datetime}"

    class Meta:
        unique_together = ('doctor', 'scheduled_datetime')