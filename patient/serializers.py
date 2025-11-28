# patient/serializers.py
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 
            'patient_id_hospital', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'gender', 
            'phone_number', 
            'address', 
            'blood_group', 
            'created_at'
        ]
        read_only_fields = ['id', 'patient_id_hospital', 'created_at']