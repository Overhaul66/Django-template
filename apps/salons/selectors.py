from django.db.models import Count, Q, F
from django.db.models.functions import ACos, Cos, Radians, Sin
from decimal import Decimal
from .models import Salon

def list_salons(
    city=None,
    service_name=None,
    gender_type=None,
    min_rating=None,
    ordering=None,
    lat=None,
    lon=None
):
    queryset = Salon.objects.filter(status='ACTIVE')
    
    if city:
        queryset = queryset.filter(city__iexact=city)
        
    if service_name:
        # Avoid duplicate salon entries when filtering by service
        queryset = queryset.filter(services__name__icontains=service_name, services__is_active=True).distinct()
        
    if gender_type:
        queryset = queryset.filter(gender_type=gender_type)
        
    if min_rating:
        queryset = queryset.filter(rating__gte=Decimal(str(min_rating)))
        
    # Ordering logic
    if ordering == 'highest_rated':
        queryset = queryset.order_by('-rating', '-created_at')
    elif ordering == 'most_popular':
        queryset = queryset.annotate(num_appointments=Count('appointments')).order_by('-num_appointments', '-created_at')
    elif ordering == 'newest':
        queryset = queryset.order_by('-created_at')
    elif ordering == 'nearest' and lat is not None and lon is not None:
        # Geodetic distance formula using spherical law of cosines
        try:
            lat_rad = Radians(Decimal(str(lat)))
            lon_rad = Radians(Decimal(str(lon)))
            
            queryset = queryset.annotate(
                distance=6371 * ACos(
                    Sin(lat_rad) * Sin(Radians(F('latitude'))) +
                    Cos(lat_rad) * Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - lon_rad)
                )
            ).order_by('distance')
        except Exception:
            # Fallback to default ordering if math functions fail or lat/lon values are malformed
            queryset = queryset.order_by('-created_at')
    else:
        queryset = queryset.order_by('-created_at')
        
    return queryset

def get_salon_by_id(salon_id) -> Salon:
    return Salon.objects.get(id=salon_id)
