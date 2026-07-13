from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'salon', 'employee', 'service', 'appointment_date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'appointment_date', 'salon')
    search_fields = ('customer__user__email', 'employee__user__email', 'salon__name')
