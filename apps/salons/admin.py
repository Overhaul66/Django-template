from django.contrib import admin
from .models import Salon, SalonImage, SalonService, BusinessHours

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'city', 'phone', 'opening_time', 'closing_time', 'rating', 'status')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('city', 'status', 'gender_type')
    search_fields = ('name', 'description', 'city')


@admin.register(SalonService)
class SalonServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'duration_minutes', 'price', 'is_active')
    list_filter = ('is_active', 'salon')
    search_fields = ('name', 'description')


@admin.register(SalonImage)
class SalonImageAdmin(admin.ModelAdmin):
    list_display = ('salon', 'caption', 'order')


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('salon', 'weekday', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('weekday', 'is_closed')
