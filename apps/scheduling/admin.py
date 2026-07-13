from django.contrib import admin
from .models import EmployeeAvailability

@admin.register(EmployeeAvailability)
class EmployeeAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('date', 'status', 'employee__salon')
    search_fields = ('employee__user__email', 'employee__user__first_name', 'employee__user__last_name')
