# bloodbank/serializers.py

from rest_framework import serializers

from .models import BloodDonor, BloodBag, BloodRequest
 
class BloodDonorSerializer(serializers.ModelSerializer):

    class Meta:

        model = BloodDonor

        fields = '__all__'
 
class BloodBagSerializer(serializers.ModelSerializer):

    donor_name = serializers.ReadOnlyField(source='donor.name')

    class Meta:

        model = BloodBag

        fields = '__all__'
 
class BloodRequestSerializer(serializers.ModelSerializer):

    patient_name = serializers.ReadOnlyField(source='patient.first_name')

    doctor_name = serializers.ReadOnlyField(source='doctor.user.first_name')

    bag_details = BloodBagSerializer(source='issued_bag', read_only=True)
 
    class Meta:

        model = BloodRequest

        fields = [

            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',

            'required_blood_group', 'required_component', 'units_required',

            'request_date', 'status', 'issued_bag', 'bag_details'

        ]
 
