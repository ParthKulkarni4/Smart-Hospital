from django.db import models
from patient.models import Patient
from doctor.models import Doctor
from appointments.models import Appointment

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    # Optional: Link to specific appointment
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
    # Clinical Notes
    symptoms = models.TextField(help_text="Chief Complaints")
    diagnosis = models.TextField()
    treatment_plan = models.TextField(blank=True, null=True)
    
    # Vitals (Basic)
    bp = models.CharField(max_length=20, blank=True, null=True, help_text="Blood Pressure (e.g. 120/80)")
    pulse = models.CharField(max_length=10, blank=True, null=True)
    temperature = models.CharField(max_length=10, blank=True, null=True)
    weight = models.CharField(max_length=10, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record: {self.patient.first_name} - {self.date.date()}"


class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100) # e.g., "1-0-1" or "500mg"
    frequency = models.CharField(max_length=100) # e.g., "After Food"
    duration = models.CharField(max_length=50) # e.g., "5 Days"
    
    def __str__(self):
        return f"{self.medicine_name} ({self.dosage})"