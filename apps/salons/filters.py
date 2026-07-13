import django_filters
from .models import Salon, SalonService

class SalonFilter(django_filters.FilterSet):
    service = django_filters.CharFilter(field_name='services__name', lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='iexact')
    gender = django_filters.CharFilter(field_name='gender_type', lookup_expr='exact')
    rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')

    class Meta:
        model = Salon
        fields = ['city', 'service', 'gender', 'rating']


class SalonServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = SalonService
        fields = ['min_price', 'max_price', 'is_active']
