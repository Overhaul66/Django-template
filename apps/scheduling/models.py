import uuid
from django.db import models
from apps.users.models import SalonEmployee

class EmployeeAvailability(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('BOOKED', 'Booked'),
        ('BREAK', 'Break'),
        ('LEAVE', 'Leave'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(SalonEmployee, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    class Meta:
        db_table = 'employee_availabilities'
        verbose_name_plural = 'Employee Availabilities'

    def __str__(self):
        return f"{self.employee.user.email} - {self.date} [{self.start_time} - {self.end_time}] ({self.status})"
