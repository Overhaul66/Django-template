from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalonViewSet, SalonServiceViewSet

router = DefaultRouter()
router.register('salons', SalonViewSet, basename='salon')
router.register('services', SalonServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]
