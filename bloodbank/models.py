# bloodbank/models.py

from django.db import models

from patient.models import Patient

from doctor.models import Doctor
 
class BloodDonor(models.Model):

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    BLOOD_GROUPS = [

        ('A+', 'A+'), ('A-', 'A-'),

        ('B+', 'B+'), ('B-', 'B-'),

        ('AB+', 'AB+'), ('AB-', 'AB-'),

        ('O+', 'O+'), ('O-', 'O-'),

    ]
 
    name = models.CharField(max_length=150)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)

    phone_number = models.CharField(max_length=15)

    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):

        return f"{self.name} ({self.blood_group})"
 
class BloodBag(models.Model):

    """The Inventory Item"""

    COMPONENT_CHOICES = [

        ('Whole Blood', 'Whole Blood'),

        ('Plasma', 'Plasma'),

        ('Platelets', 'Platelets'),

    ]

    STATUS_CHOICES = [

        ('Available', 'Available'),

        ('Reserved', 'Reserved'),

        ('Issued', 'Issued'),

        ('Expired', 'Expired'),

    ]
 
    donor = models.ForeignKey(BloodDonor, on_delete=models.SET_NULL, null=True)

    bag_number = models.CharField(max_length=50, unique=True) # Physical barcode ID

    blood_group = models.CharField(max_length=5, choices=BloodDonor.BLOOD_GROUPS)

    component_type = models.CharField(max_length=20, choices=COMPONENT_CHOICES, default='Whole Blood')

    volume_ml = models.PositiveIntegerField(default=350)

    collection_date = models.DateField()

    expiry_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
 
    def __str__(self):

        return f"{self.bag_number} - {self.blood_group} ({self.status})"
 
class BloodRequest(models.Model):

    """The Transaction"""

    STATUS_CHOICES = [

        ('Requested', 'Requested'),

        ('Approved', 'Approved'),

        ('Issued', 'Issued'),

        ('Rejected', 'Rejected'),

    ]
 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='blood_requests')

    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    required_blood_group = models.CharField(max_length=5, choices=BloodDonor.BLOOD_GROUPS)

    required_component = models.CharField(max_length=20, choices=BloodBag.COMPONENT_CHOICES)

    units_required = models.PositiveIntegerField(default=1)

    request_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')

    # When issued, we link to the specific bag(s). 

    # Since one request might need multiple bags, a ManyToMany is safer, 

    # but for simplicity here, we'll assume 1 request = 1 bag issuance or handle via logic.

    issued_bag = models.OneToOneField(BloodBag, on_delete=models.SET_NULL, null=True, blank=True)
 
    def __str__(self):

        return f"Req for {self.patient}: {self.required_blood_group}"

