from rest_framework import permissions

class IsSalonManager(permissions.BasePermission):
    """
    Allows access only to users with the SALON_MANAGER role (or Django staff/superusers).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role == 'SALON_MANAGER' or request.user.is_staff)
        )


class IsSalonEmployee(permissions.BasePermission):
    """
    Allows access only to users with the SALON_EMPLOYEE role (or Django staff/superusers).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role == 'SALON_EMPLOYEE' or request.user.is_staff)
        )


class IsCustomer(permissions.BasePermission):
    """
    Allows access only to users with the CUSTOMER role (or Django staff/superusers).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role == 'CUSTOMER' or request.user.is_staff)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to check if the requesting user owns the resource or is admin.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Check user ownership
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'customer'):
            return obj.customer.user == request.user

        # If the object itself is a CustomUser
        if hasattr(obj, 'email') and hasattr(obj, 'role'):
            return obj == request.user
            
        return False
