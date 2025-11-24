from rest_framework import serializers
from .models import ReceptionistProfile
from accounts.models import User
from accounts.serializers import UserSerializer


class ReceptionistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    # When sending POST/PUT use user_id only
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='user',
        queryset=User.objects.all()
    )

    class Meta:
        model = ReceptionistProfile
        fields = [
            'id',
            'user',
            'user_id',
            'employee_id',
            'shift',
            'department',
        ]
        read_only_fields = ['employee_id']
