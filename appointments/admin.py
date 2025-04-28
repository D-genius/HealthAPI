# appointments/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor_name', 'scheduled_datetime', 'status')
    list_filter = ('status', 'doctor__specialization')
    search_fields = ('patient__user__email', 'doctor__user__email')
    date_hierarchy = 'scheduled_datetime'

    def patient_name(self, obj):
        return obj.patient.user.get_full_name() if obj.patient else '-'
    patient_name.short_description = 'Patient'

    def doctor_name(self, obj):
        return obj.doctor.user.get_full_name()
    doctor_name.short_description = 'Doctor'