from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Appointment.objects.all().order_by('-appointment_date', '-start_time')
        
        # Allow filtering by date (e.g., ?date=2025-11-01)
        date_param = self.request.query_params.get('date')
        doctor_id = self.request.query_params.get('doctor_id')
        
        if date_param:
            queryset = queryset.filter(appointment_date=date_param)
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
            
        return queryset