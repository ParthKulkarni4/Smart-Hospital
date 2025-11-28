from django.db import models
from django.conf import settings

class Doctor(models.Model):
    # Link to the Shared User (Login)
    # db_constraint=False is REQUIRED because User is in DB_Shared 
    # and Doctor is in DB_Tenant. SQL cannot enforce FKs across files.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'Doctor'},
        db_constraint=False, 
        related_name='doctor_profile'
    )

    # Professional Details
    specialization = models.CharField(max_length=100) # e.g., Cardiologist
    department = models.CharField(max_length=100)     # e.g., Cardiology
    experience_years = models.PositiveIntegerField(default=0)
    
    # Financials
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Availability (Simple implementation for now)
    is_available = models.BooleanField(default=True)
    available_days = models.CharField(max_length=100, default="Mon,Tue,Wed,Thu,Fri")
    available_time_start = models.TimeField(null=True, blank=True)
    available_time_end = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # access user data via self.user
        return f"Dr. {self.user.last_name} - {self.specialization}"