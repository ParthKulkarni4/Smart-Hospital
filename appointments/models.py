from django.db import models
from patient.models import Patient
from doctor.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('NoShow', 'No Show'),
    ]

    # Foreign Keys (Same DB, so standard CASCADE/PROTECT works)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    
    # Scheduling Details
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    reason = models.TextField(blank=True, null=True) # Symptoms or reason for visit
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Optional: Indexing for faster searching by date
        indexes = [
            models.Index(fields=['appointment_date', 'status']),
        ]

    def __str__(self):
        return f"Appt: {self.patient} with {self.doctor} on {self.appointment_date}"