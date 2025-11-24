from django import forms
from django.contrib.auth import get_user_model
from patient.models import Patient

User = get_user_model()

class PatientForm(forms.ModelForm):

    # User table fields
    username = forms.CharField(max_length=150, required=True, label='Username')
    first_name = forms.CharField(max_length=150, required=True, label='First Name')
    last_name = forms.CharField(max_length=150, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=15, required=True, label='Primary Phone')

    class Meta:
        model = Patient
        fields = [
            'date_of_birth', 
            'gender',
            'phone_secondary',
            'address',
            'emergency_contact_name',
            'emergency_contact_phone',
            'insurance_provider',
            'insurance_number',
            'blood_group',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.user:
            # Populate user fields
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.phone_number

    def save(self, commit=True):
        patient = super().save(commit=False)

        # Prepare user data
        user_data = {
            'username': self.cleaned_data['username'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
            'phone': self.cleaned_data['phone'],
        }

        # If patient exists → update user
        if patient.pk:
            for attr, value in user_data.items():
                setattr(patient.user, attr, value)
            patient.user.save()

        else:
            # create new user for patient
            user_data['role'] = 'Patient'
            user_data['admin_owner'] = 'shared'   # change as needed
            user = User.objects.create_user(**user_data)
            patient.user = user
            patient.phone_number = user_data['phone']

        if commit:
            patient.save()

        return patient
