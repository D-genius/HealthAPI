# doctors/admin.py
from django.contrib import admin
from .models import Doctor, Availability

class DoctorAvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone')
    inlines = [DoctorAvailabilityInline]
    search_fields = ('user__email', 'specialization')
    
    def formatted_contact(self, obj):
        return obj.contact_details[:30] + '...' if len(obj.contact_details) > 30 else obj.phone
    formatted_contact.short_description = 'Contact Info'

@admin.register(Availability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_datetime', 'end_datetime', 'is_available')
    list_filter = ('is_available', 'doctor__specialization')