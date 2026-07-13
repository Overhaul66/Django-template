from .models import EmployeeAvailability

def get_employee_availability(employee, date):
    return EmployeeAvailability.objects.filter(employee=employee, date=date)

def list_employee_availabilities(employee, start_date, end_date):
    return EmployeeAvailability.objects.filter(
        employee=employee,
        date__range=[start_date, end_date]
    ).order_by('date', 'start_time')
