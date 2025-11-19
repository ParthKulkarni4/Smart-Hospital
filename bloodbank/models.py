from django.db import models
class BloodUnit(models.Model):
    blood_group = models.CharField(max_length=5)
    units = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.blood_group} - {self.units} units"

# -------------------------------------------

# bloodbank/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from patients.models import Patient

# Blood group choices
BLOOD_GROUP_CHOICES = [
    ("A+", "A+"), ("A-", "A-"),
    ("B+", "B+"), ("B-", "B-"),
    ("AB+", "AB+"), ("AB-", "AB-"),
    ("O+", "O+"), ("O-", "O-"),
]

GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]

AGE_CHOICES = [(i, i) for i in range(18, 80)] 

class Donor(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField(choices=AGE_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    phone = models.CharField(max_length=10,blank=True)
    address = models.TextField(blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, unique=True)
    units = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # units can be fractional if needed

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['blood_group']

    def __str__(self):
        return f"{self.blood_group}: {self.units} units"


class BloodIssue(models.Model):
    # assume a Patient model exists in some app named 'patients'
    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='blood_issues')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_issued = models.DecimalField(max_digits=6, decimal_places=2)
    issue_date = models.DateTimeField(default=timezone.now)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    bill_no = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue {self.id} - {self.patient} - {self.blood_group} ({self.units_issued})"

class BloodRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    quantity_ml = models
    .PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected"), ("Completed", "Completed")],
        default="Pending"
    )
    request_date = models.DateTimeField(default=timezone.now)
    approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request #{self.id} - {self.patient.name}"

medical_issues = models.BooleanField(default=False)
