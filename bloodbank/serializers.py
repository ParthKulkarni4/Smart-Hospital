from rest_framework import serializers
from .models import BloodUnit
class BloodUnitSerializer(serializers.ModelSerializer):
    class Meta: model=BloodUnit; fields='__all__'

# bloodbank/serializers.py
from rest_framework import serializers
from .models import Donor, BloodInventory, BloodIssue, BLOOD_GROUP_CHOICES
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_units(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory units cannot be negative.")
        return value


class BloodIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodIssue
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_units_issued(self, value):
        if value <= 0:
            raise serializers.ValidationError("Units issued must be greater than zero.")
        return value

    def validate(self, data):
        # Ensure blood_group is valid
        valid_groups = [g[0] for g in BLOOD_GROUP_CHOICES]
        if data.get('blood_group') not in valid_groups:
            raise serializers.ValidationError({"blood_group": "Invalid blood group."})
        return data
