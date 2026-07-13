from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer, SalonEmployee, SalonManager

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_verified')
    list_filter = ('role', 'is_active', 'is_staff', 'is_verified')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'role', 'first_name', 'last_name', 'is_active', 'is_verified'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'preferred_notification', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(SalonManager)
class SalonManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(SalonEmployee)
class SalonEmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'position', 'is_available', 'employment_date')
    list_filter = ('is_available', 'salon')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'position')
