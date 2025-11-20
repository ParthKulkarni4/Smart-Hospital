from rest_framework import serializers
from .models import ReceptionistProfile
from django.contrib.auth import get_user_model
from accounts.models import User

User = get_user_model()


# Serializer for ReceptionistProfile
class ReceptionistProfileSerializer(serializers.ModelSerializer):
    user = User(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, source='user', queryset=User.objects.all())

    class Meta:
        model = ReceptionistProfile
        fields = ['id', 'user', 'user_id', 'employee_id', 'shift', 'department']
        read_only_fields = ['employee_id']
