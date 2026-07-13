from rest_framework import serializers
from apps.users.models import SalonEmployee
from apps.salons.models import Salon

class ManageEmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    phone = serializers.CharField(source='user.phone', required=False, allow_blank=True)
    is_active = serializers.BooleanField(source='user.is_active', required=False)
    salon_name = serializers.CharField(source='salon.name', read_only=True)

    class Meta:
        model = SalonEmployee
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone', 'salon', 
            'salon_name', 'position', 'bio', 'is_available', 'employment_date', 
            'is_active', 'created_at'
        )
        read_only_fields = ('id', 'email', 'created_at')


class CreateEmployeeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, default="", allow_blank=True)
    last_name = serializers.CharField(required=False, default="", allow_blank=True)
    phone = serializers.CharField(required=False, default="", allow_blank=True)
    salon_id = serializers.PrimaryKeyRelatedField(queryset=Salon.objects.all(), source='salon')
    position = serializers.CharField()
    bio = serializers.CharField(required=False, default="", allow_blank=True)


class ResetEmployeePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
