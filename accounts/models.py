# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SuperAdmin')
        extra_fields.setdefault('admin_owner', 'shared') # SuperAdmin is on the shared DB

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    # Define roles as per your project summary
    ROLE_CHOICES = [
        ('SuperAdmin', 'SuperAdmin'), # Manages all hospitals
        ('Admin', 'Admin'),           # Owns a hospital (tenant)
        ('FrontOffice', 'FrontOffice'),
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Billing', 'Billing'),
        ('Pharmacy', 'Pharmacy'),
        ('Inventory', 'Inventory'),
        ('Pathology', 'Pathology'),
        ('Radiology', 'Radiology'),
        ('Ambulance', 'Ambulance'),
        ('HR', 'HR'),
        ('BloodBank', 'BloodBank'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # This is the KEY to your multi-tenant architecture.
    # It tells the DB router which database this user's data belongs to.
    # For a SuperAdmin, this could be 'shared' or 'default'.
    # For a hospital Admin and all their staff, this will be the tenant DB name
    # (e.g., 'hospital_apollo', 'hospital_max').
    admin_owner = models.CharField(max_length=100, help_text="The database identifier for the tenant.")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Required for Django admin
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'admin_owner']

    def __str__(self):
        return f"{self.email} ({self.role} @ {self.admin_owner})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name