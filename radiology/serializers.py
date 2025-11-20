from rest_framework import serializers
from .models import RadiologyTest, RadiologyReport, RadiologyRecord

class RadiologyTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyTest
        fields = "__all__"
        read_only_fields = ("id",)


class RadiologyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyReport
        fields = "__all__"
        read_only_fields = ("id", "created_by", "created_at", "finalized_by", "finalized_at")


class RadiologyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyRecord
        fields = "__all__"
        read_only_fields = ("id", "uploaded_by", "uploaded_at")
