from django.contrib import admin
from .models import Ambulance, AmbulanceCall


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ("vehicle_number", "driver_name", "driver_phone", "status", "current_lat", "current_long")
    search_fields = ("vehicle_number", "driver_name")
    list_filter = ("status",)


@admin.register(AmbulanceCall)
class AmbulanceCallAdmin(admin.ModelAdmin):
    list_display = ("patient", "ambulance", "status", "created_at", "completed_at")
    search_fields = ("patient__user__first_name", "ambulance__vehicle_number")
    list_filter = ("status", "created_at")