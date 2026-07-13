import django_filters
from .models import Appointment

class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['salon', 'employee', 'status', 'appointment_date']
