from rest_framework import permissions

class IsEmployeeOrManager(permissions.BasePermission):
    """
    Employees can manage their own availability, managers can manage their salon's employee availabilities.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        if request.user.role == 'SALON_EMPLOYEE' and hasattr(request.user, 'employee_profile'):
            return obj.employee == request.user.employee_profile
            
        if request.user.role == 'SALON_MANAGER' and hasattr(request.user, 'manager_profile'):
            return obj.employee.salon.manager == request.user.manager_profile
            
        return False
