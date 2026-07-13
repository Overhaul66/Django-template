import django_filters
from .models import EmployeeAvailability

class EmployeeAvailabilityFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeeAvailability
        fields = ['employee', 'date', 'status']
