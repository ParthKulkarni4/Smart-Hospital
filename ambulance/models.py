# from django.db import models
# class Ambulance(models.Model):
#     STATUS_CHOICES = [
#         ('available', 'Available'),
#         ('busy', 'Busy'),
#         ('maintenance', 'Maintenance'),
#     ]
#     vehicle_no = models.CharField(max_length=50)
#     driver_name = models.CharField(max_length=100)
#     contact = models.CharField(max_length=20, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
#     def __str__(self): return self.vehicle_no



# class AmbulanceTrip(models.Model):
#     STATUS_CHOICES = [
#         ('requested', 'Requested'),
#         ('dispatched', 'Dispatched'),
#         ('arrived', 'Arrived'),
#         ('completed', 'Completed'),
#     ]

#     ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
#     patient = models.ForeignKey('patient.Patient', on_delete=models.SET_NULL, null=True)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
#     booked_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='booked_ambulance_trips')
#     def __str__(self): return f"{self.ambulance or 'Unassigned'} trip for {self.patient or 'Unknown Patient'}"











# ambulance/models.py

from django.db import models

from accounts.models import User
from patient.models import Patient
 
class Ambulance(models.Model):

    STATUS_CHOICES = [

        ('Available', 'Available'),

        ('OnTrip', 'On Trip'),

        ('Maintenance', 'Maintenance'),

    ]

    vehicle_number = models.CharField(max_length=20, unique=True) # e.g., MH-12-AB-1234

    driver_name = models.CharField(max_length=100)

    driver_phone = models.CharField(max_length=15, default="+91 ")

    # Tracking Data (Updated via API)

    current_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    current_long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    last_location_update = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):

        return f"{self.vehicle_number} ({self.driver_name})"
 
class AmbulanceCall(models.Model):

    STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('Dispatched', 'Dispatched'),

        ('Completed', 'Completed'),

        ('Cancelled', 'Cancelled'),

    ]
 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ambulance_calls')

    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True)

    pickup_address = models.TextField()

    drop_address = models.TextField(default="Hospital Base")

    # Financials

    trip_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Timestamps

    created_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    booked_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="ambulance_bookings"    # Add this filed for booking user
)

 
    def __str__(self):

        return f"Trip for {self.patient} - {self.status}"
 