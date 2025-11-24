from rest_framework import viewsets, permissions, filters
from .models import ReceptionistProfile
from .serializers import ReceptionistProfileSerializer
from accounts.permissions import IsReceptionistOrAdmin



from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from datetime import date, timedelta

from doctor.models import Doctor
from patient.models import Patient
from appointments.models import Appointment
from billing.models import Bill
from django.db.models import Count
# from pathology.models import PathologyReport
# from radiology.models import RadiologyReport



class ReceptionistProfileViewSet(viewsets.ModelViewSet):
    queryset = ReceptionistProfile.objects.select_related('user').all()
    serializer_class = ReceptionistProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsReceptionistOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [p() for p in permission_classes]










  ####   Receptionist Dashboard API View   ####
#Recpeptionist Dashboard API view to provide statistics and data for receptionist users 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated ])
def receptionist_dashboard(request):
    today = date.today()
    week_ago = today - timedelta(days=7)


#  Count 
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.filter(appointment_date__isnull=False).count()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    week_appointments = Appointment.objects.filter(appointment_date__gte=week_ago, appointment_date__lte=today).count()
    upcoming_appointments = Appointment.objects.filter(appointment_date__gt=today).count()
    past_appointments = Appointment.objects.filter(appointment_date__lt=today).count()
    total_bills = 0
    total_pharmacy_orders = 0  
    # total_pathology_tests = PathologyReport.objects.count() 
    # total_radiology_tests = RadiologyReport.objects.count()  
    total_doctors = Doctor.objects.count() 
    

    # apointments in last 7  Days
    appointment_last_week=(
        Appointment.objects
        .filter(appointment_date__range =(week_ago, today))
        .values('appointment_date')
        .annotate(count=Count('id'))    
        .order_by('appointment_date')
    )

    chart_labels=[]
    chart_data=[]
     # Fill all 7 days [even with zero appointments]
    for i in  range(7):
        day= week_ago + timedelta(days=i)
        count = next((x['total'] for x in appointment_last_week if x['appointment_date'] == day), 0)
        chart_labels.append(day.strftime('%Y-%m-%d'))
        chart_data.append(count)


    data = {
        'stats':{
        'patients': total_patients,
        'appointments': {
            'total': total_appointments,
            'today': today_appointments,
            'this_week': week_appointments,
            'upcoming': upcoming_appointments,
            'past': past_appointments
        },
        "billing":total_bills,
        'doctors': total_doctors,
        'pharmacy_orders': total_pharmacy_orders,
        # 'pathology_tests': total_pathology_tests,
        # 'radiology_tests': total_radiology_tests,
        },

        "chart":{
            "labels": chart_labels,
            "data": chart_data
        }
    }    

    return Response({'success': True, 'data': data})


    

