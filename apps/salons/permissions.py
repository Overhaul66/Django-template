from rest_framework import permissions

class IsSalonOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows safe methods for anyone, but write methods require the user to be 
    the manager who owns the salon (or a superuser).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True
            
        if request.user.role == 'SALON_MANAGER' and hasattr(request.user, 'manager_profile'):
            manager_profile = request.user.manager_profile
            # If checking Salon object
            if hasattr(obj, 'manager'):
                return obj.manager == manager_profile
            # If checking nested Salon objects (SalonService, BusinessHours, SalonImage)
            if hasattr(obj, 'salon'):
                return obj.salon.manager == manager_profile
                
        return False
