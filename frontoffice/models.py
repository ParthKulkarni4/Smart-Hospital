from django.db import models
from django.conf import settings

from appointments.serializers import AppointmentSerializer



class ReceptionistProfile(models.Model):

    SHIFT_CHOICES = (
        ("Morning", "Morning"),
        ("Evening", "Evening"),
        ("Night", "Night"),
        ("Full Day", "Full Day"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='receptionist_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True, blank=True)

    shift = models.CharField(max_length=50, choices=SHIFT_CHOICES, blank=True)
    
    department = models.CharField(max_length=100, blank=True ,choices=(
        ("Front office", "Front office"),   
        ("Billing", "Billing"),
        ("OPD", "OPD"), 
        ("Emergency", "Emergency"),    
    )) 

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.employee_id})"







