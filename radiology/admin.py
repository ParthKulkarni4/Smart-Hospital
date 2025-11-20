from django.contrib import admin
from .models import RadiologyTest, RadiologyReport, RadiologyRecord

@admin.register(RadiologyTest)
class RadiologyTestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "modality", "is_active")
    search_fields = ("name", "code", "description")
    list_filter = ("modality", "is_active")

@admin.register(RadiologyReport)
class RadiologyReportAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_name", "test", "status", "created_by", "created_at", "finalized_by", "finalized_at")
    search_fields = ("patient_name", "findings", "test__name")
    list_filter = ("status", "test__modality")

@admin.register(RadiologyRecord)
class RadiologyRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_name", "test", "uploaded_by", "uploaded_at")
    search_fields = ("patient_name",)
    list_filter = ("test",)
