from django.contrib import admin
# Register models here

#-------------------------------------------------
# bloodbank/admin.py
from django.contrib import admin
from .models import Donor, BloodInventory, BloodIssue

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'phone', 'last_donation_date')

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units')

@admin.register(BloodIssue)
class BloodIssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'blood_group', 'units_issued', 'issue_date', 'issued_by')
