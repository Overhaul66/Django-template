from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeAvailabilityViewSet, MyScheduleView

router = DefaultRouter()
router.register('availabilities', EmployeeAvailabilityViewSet, basename='availability')

urlpatterns = [
    path('my/schedule/', MyScheduleView.as_view(), name='my_schedule'),
    path('', include(router.urls)),
]
