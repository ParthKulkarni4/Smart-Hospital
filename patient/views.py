from django.shortcuts import render
# patient/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Patients to be viewed or edited.
    The database router automatically filters this query 
    based on the request.user.admin_owner.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        # MAGIC HAPPENS HERE:
        # This looks like it fetches ALL patients in the world.
        # But your Router intercepts this and routes it to 
        # 'db_hospital_a.sqlite3' (or whichever hospital the user belongs to).
        return Patient.objects.all().order_by('-created_at')