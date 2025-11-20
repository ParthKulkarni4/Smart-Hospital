from django.contrib import admin
# Register models here
from .models import Ambulance, AmbulanceTrip


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle_no', 'driver_name', 'contact','status')
    list_filter = ()
    search_fields = ('vehicle_no', 'driver_name')

@admin.register(AmbulanceTrip)
class AmbulanceTripAdmin(admin.ModelAdmin):
    list_display = ('ambulance', 'patient', 'start_time', 'end_time','status','booked_by')
    list_filter = ()
    search_fields = ('ambulance__vehicle_no', 'patient__user__first_name', 'patient__user__last_name')
    readonly_fields = ('booked_by',)