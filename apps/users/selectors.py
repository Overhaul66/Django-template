from .models import CustomUser, Customer, SalonEmployee, SalonManager

def get_user_by_id(user_id) -> CustomUser:
    return CustomUser.objects.get(id=user_id)

def get_customer_by_user(user: CustomUser) -> Customer:
    return user.customer_profile

def get_employee_by_user(user: CustomUser) -> SalonEmployee:
    return user.employee_profile

def get_manager_by_user(user: CustomUser) -> SalonManager:
    return user.manager_profile
