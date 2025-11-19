from rest_framework import serializers
from .models import Appointment
from patient.serializers import PatientSerializer
from doctor.serializers import DoctorSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    # Nested serializers for reading (to show full names in JSON)
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 
            'patient', 'patient_details', # Write ID, Read Object
            'doctor', 'doctor_details',   # Write ID, Read Object
            'appointment_date', 
            'start_time', 
            'end_time', 
            'status', 
            'reason'
        ]

    def validate(self, data):
        """
        Check for double booking.
        """
        # Only check if we are creating or updating schedule details
        doctor = data.get('doctor')
        date = data.get('appointment_date')
        start = data.get('start_time')
        
        if not (doctor and date and start):
            return data # Allow partial updates that don't change time

        # Check if any Scheduled appointment exists for this doctor, date, and time
        # We exclude the current instance (if updating)
        existing_appt = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            start_time=start,
            status='Scheduled'
        )
        
        # If updating, exclude self
        if self.instance:
            existing_appt = existing_appt.exclude(pk=self.instance.pk)

        if existing_appt.exists():
            raise serializers.ValidationError({
                "start_time": "This doctor is already booked for this time slot."
            })

        return data