from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeManagementViewSet

router = DefaultRouter()
router.register('employees', EmployeeManagementViewSet, basename='employee-manage')

urlpatterns = [
    path('', include(router.urls)),
]
