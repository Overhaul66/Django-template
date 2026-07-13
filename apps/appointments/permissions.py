from rest_framework import permissions

class AppointmentAccessPermission(permissions.BasePermission):
    """
    Restricts access to appointment records:
    - Customer: can only access their own appointments.
    - Employee: can only access appointments assigned to them.
    - Manager: can access any appointments booked at their salons.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        # Manager ownership check
        if request.user.role == 'SALON_MANAGER' and hasattr(request.user, 'manager_profile'):
            return obj.salon.manager == request.user.manager_profile
            
        # Employee ownership check
        if request.user.role == 'SALON_EMPLOYEE' and hasattr(request.user, 'employee_profile'):
            return obj.employee == request.user.employee_profile
            
        # Customer ownership check
        if request.user.role == 'CUSTOMER' and hasattr(request.user, 'customer_profile'):
            return obj.customer == request.user.customer_profile
            
        return False
