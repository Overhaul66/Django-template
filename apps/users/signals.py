from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser, Customer, SalonManager, SalonEmployee

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'CUSTOMER':
            Customer.objects.get_or_create(user=instance)
        elif instance.role == 'SALON_MANAGER':
            SalonManager.objects.get_or_create(user=instance)
        elif instance.role == 'SALON_EMPLOYEE':
            # Create a default profile shell. The manager will fill the remaining details (salon, position).
            SalonEmployee.objects.get_or_create(
                user=instance,
                defaults={
                    'position': 'Staff',
                    'employment_date': timezone.now().date()
                }
            )
