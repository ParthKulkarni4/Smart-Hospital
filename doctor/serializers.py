from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

class DoctorUserSerializer(serializers.ModelSerializer):
    """
    A mini-serializer to show user details inside the Doctor object
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class DoctorSerializer(serializers.ModelSerializer):
    # Nest the user data
    user_details = DoctorUserSerializer(source='user', read_only=True)
    
    # For creating a doctor, we just pass the user ID
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='Doctor'), 
        source='user',
        write_only=True
    )

    class Meta:
        model = Doctor
        fields = [
            'id', 
            'user_id',       # Used for writing (creating)
            'user_details',  # Used for reading (viewing)
            'specialization', 
            'department', 
            'experience_years', 
            'consultation_fee',
            'is_available',
            'available_days',
            'available_time_start',
            'available_time_end'
        ]