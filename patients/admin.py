# patients/admin.py
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'insurance_number_short', 'phone_short')
    search_fields = ('user__email', 'id_number', 'insurance_number')
    
    def insurance_number_short(self, obj):
        return obj.insurance_number[:6] + '...' if len(obj.insurance_number) > 6 else obj.insurance_number
    insurance_number_short.short_description = 'Insurance No.'
    
    def phone_short(self, obj):
        return obj.contact_details[:30] + '...' if len(obj.contact_details) > 30 else obj.contact_details
    phone_short.short_description = 'Contact Info'