from apps.users.models import SalonEmployee
from apps.salons.models import Salon

def list_employees_for_manager(manager):
    salons = Salon.objects.filter(manager=manager)
    return SalonEmployee.objects.filter(salon__in=salons).order_by('-created_at')

def get_employee_by_id_for_manager(manager, employee_id):
    salons = Salon.objects.filter(manager=manager)
    return SalonEmployee.objects.get(id=employee_id, salon__in=salons)
