from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'admin_owner',
            'is_active',
            'is_staff',
            'date_joined',
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

