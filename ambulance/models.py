from django.db import models
class Ambulance(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('maintenance', 'Maintenance'),
    ]
    vehicle_no = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    def __str__(self): return self.vehicle_no



class AmbulanceTrip(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('dispatched', 'Dispatched'),
        ('arrived', 'Arrived'),
        ('completed', 'Completed'),
    ]

    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.Patient', on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    booked_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='booked_ambulance_trips')
    def __str__(self): return f"{self.ambulance or 'Unassigned'} trip for {self.patient or 'Unknown Patient'}"
