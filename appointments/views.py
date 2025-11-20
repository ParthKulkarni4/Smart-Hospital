from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    # ---------------------------------------
    # def get_queryset(self):
    #     queryset = Appointment.objects.all().order_by('-appointment_date', '-start_time')
    #     
    #     # Allow filtering by date (e.g., ?date=2025-11-01)
    #     date_param = self.request.query_params.get('date')
    #     doctor_id = self.request.query_params.get('doctor_id')
    #     
    #     if date_param:
    #         queryset = queryset.filter(appointment_date=date_param)
    #     
    #     if doctor_id:
    #         queryset = queryset.filter(doctor_id=doctor_id)
    # 
    #     return queryset
    #

    # -----------------------------
    def get_queryset(self):
        """
        Base queryset: all appointments ordered newest-first.
        - If ?date=... is provided, filter by date.
        - If the logged-in user is a doctor, ALWAYS restrict to that doctor.
        - Otherwise, if ?doctor_id=... is provided, filter by doctor_id.
        """
        queryset = Appointment.objects.all().order_by('-appointment_date', '-start_time')

        # basic filters
        date_param = self.request.query_params.get('date')
        doctor_id_param = self.request.query_params.get('doctor_id')

        if date_param:
            queryset = queryset.filter(appointment_date=date_param)

        # restrict doctors to their own appointments
        user = self.request.user
        doctor_role_name = getattr(getattr(user, 'role', None), 'name', None)

        if doctor_role_name and str(doctor_role_name).lower() == 'doctor':
            queryset = queryset.filter(doctor=user)
            return queryset  # doctor cannot see other doctors' appointments

        # non-doctors (admin, staff) can still filter by doctor_id
        if doctor_id_param:
            queryset = queryset.filter(doctor_id=doctor_id_param)

        return queryset
