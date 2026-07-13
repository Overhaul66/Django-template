from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from .models import CustomUser

def register_user(email, password, role, first_name="", last_name="", phone="", profile_picture=None, **profile_fields):
    if role not in dict(CustomUser.ROLE_CHOICES):
        raise ValidationError({"role": "Invalid role selected."})
    
    if CustomUser.objects.filter(email=email).exists():
        raise ValidationError({"email": "A user with this email already exists."})
        
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        role=role,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        profile_picture=profile_picture
    )
    
    # Update profile fields (the signal created the profile shells)
    if role == 'CUSTOMER' and hasattr(user, 'customer_profile'):
        customer = user.customer_profile
        for k, v in profile_fields.items():
            if hasattr(customer, k) and v is not None:
                setattr(customer, k, v)
        customer.save()
    elif role == 'SALON_EMPLOYEE' and hasattr(user, 'employee_profile'):
        employee = user.employee_profile
        for k, v in profile_fields.items():
            if hasattr(employee, k) and v is not None:
                setattr(employee, k, v)
        employee.save()
        
    return user

def change_user_password(user, old_password, new_password):
    if not user.check_password(old_password):
        raise ValidationError({"old_password": "Old password is incorrect."})
    user.set_password(new_password)
    user.save()
    return user

def request_password_reset(email):
    try:
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return uid, token
    except CustomUser.DoesNotExist:
        # Silent return to prevent email enumeration
        return None, None

def reset_user_password(uidb64, token, new_password):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        raise ValidationError({"token": "Invalid or expired reset link."})
        
    if not default_token_generator.check_token(user, token):
        raise ValidationError({"token": "Invalid or expired reset token."})
        
    user.set_password(new_password)
    user.save()
    return user
