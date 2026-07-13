import datetime
from django.db.models import Sum
from .models import Appointment

def get_customer_appointments(customer):
    return Appointment.objects.filter(customer=customer).order_by('-appointment_date', '-start_time')

def get_employee_appointments(employee, date=None):
    queryset = Appointment.objects.filter(employee=employee)
    if date:
        queryset = queryset.filter(appointment_date=date)
    return queryset.order_by('appointment_date', 'start_time')

def get_manager_dashboard_data(manager):
    from apps.salons.models import Salon
    salons = Salon.objects.filter(manager=manager)
    today = datetime.date.today()
    
    appointments = Appointment.objects.filter(salon__in=salons)
    
    today_appointments = appointments.filter(appointment_date=today)
    pending_count = today_appointments.filter(status='PENDING').count()
    confirmed_count = today_appointments.filter(status='CONFIRMED').count()
    completed_count = today_appointments.filter(status='COMPLETED').count()
    
    today_revenue = today_appointments.filter(status='COMPLETED').aggregate(total=Sum('service__price'))['total'] or 0.0
    total_revenue = appointments.filter(status='COMPLETED').aggregate(total=Sum('service__price'))['total'] or 0.0
    
    return {
        "today_summary": {
            "pending": pending_count,
            "confirmed": confirmed_count,
            "completed": completed_count,
            "revenue": today_revenue
        },
        "total_revenue": total_revenue,
        "salons_count": salons.count(),
        # We will serialize this in the view
        "recent_appointments": Appointment.objects.filter(salon__in=salons).order_by('-created_at')[:10]
    }
