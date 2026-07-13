import datetime
from django.core.exceptions import ValidationError
from apps.salons.models import BusinessHours
from .models import EmployeeAvailability

def generate_employee_availability(employee, date):
    """
    Checks if availability exists for the employee on the given date.
    If not, creates an AVAILABLE slot based on the salon's business hours.
    """
    # Check if availability records already exist for this date
    if EmployeeAvailability.objects.filter(employee=employee, date=date).exists():
        return
        
    weekday = date.weekday()
    try:
        hours = BusinessHours.objects.get(salon=employee.salon, weekday=weekday)
        opening = hours.opening_time
        closing = hours.closing_time
        is_closed = hours.is_closed
    except BusinessHours.DoesNotExist:
        # Use default salon hours as fallback
        opening = employee.salon.opening_time
        closing = employee.salon.closing_time
        is_closed = False
        
    if is_closed:
        # Create a CLOSED slot if salon is closed, or do nothing
        return
        
    # Create the default available slot
    EmployeeAvailability.objects.create(
        employee=employee,
        date=date,
        start_time=opening,
        end_time=closing,
        status='AVAILABLE'
    )
