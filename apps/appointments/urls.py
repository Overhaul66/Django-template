from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    ManagerDashboardView,
    EmployeeAppointmentsView,
    EmployeeAppointmentStatusView
)

router = DefaultRouter()
router.register('appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('manager/dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('my/appointments/', EmployeeAppointmentsView.as_view(), name='employee_appointments'),
    path('my/appointments/<uuid:pk>/status/', EmployeeAppointmentStatusView.as_view(), name='employee_appointment_status'),
    path('', include(router.urls)),
]
