# patient/models.py
from django.db import models
from django.conf import settings

# Get the User model from settings (best practice)
# This will be your 'accounts.User' model from Step 1
User = settings.AUTH_USER_MODEL

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # Link to the User model (for portal login)
    # This is nullable because a patient record can be created by
    # FrontOffice before the patient creates a login account.
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'Patient'}
    )

    # Basic Demographic Details (as per your summary)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    
    # Medical Information
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # Record keeping
    # This ID is the one used internally by the hospital
    patient_id_hospital = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"
    
    def save(self, *args, **kwargs):
        # Auto-generate a patient ID if one isn't provided
        if not self.patient_id_hospital:
            # Simple ID generation: 'PAT' + primary key.
            # We save first to get a PK (id).
            super().save(*args, **kwargs) # Save to get self.id
            self.patient_id_hospital = f"PAT{self.id:06d}"
            # We must save again to store the patient_id_hospital
            # We only pass the 'update_fields' to avoid re-running save logic
            kwargs.pop('force_insert', None) # Not relevant on second save
            super().save(update_fields=['patient_id_hospital'], *args, **kwargs)
        else:
            super().save(*args, **kwargs)