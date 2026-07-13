from rest_framework import serializers
from .models import EmployeeAvailability

class EmployeeAvailabilitySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeAvailability
        fields = ('id', 'employee', 'employee_name', 'date', 'start_time', 'end_time', 'status')
