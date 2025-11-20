
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Ambulance, AmbulanceTrip
from patient.models import Patient

@login_required
def index(request):
    ambulances = Ambulance.objects.all()
    trips = AmbulanceTrip.objects.select_related('ambulance', 'patient', 'booked_by').all()
    patients = Patient.objects.select_related('user').all()
    return render(request, 'ambulance/index.html', {
        'ambulances': ambulances,
        'trips': trips,
        'patients': patients
    })

@login_required
def trips(request):
    trips = AmbulanceTrip.objects.select_related('ambulance', 'patient', 'booked_by').all()
    return render(request, 'ambulance/trips.html', {'trips': trips})

@login_required
def create_trip(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        ambulance_id = request.POST.get('ambulance')
        start_time = request.POST.get('start_time')

        try:
            patient = get_object_or_404(Patient, id=patient_id)
            ambulance = get_object_or_404(Ambulance, id=ambulance_id)

            # Check if ambulance is available
            if ambulance.status != 'available':
                messages.error(request, f'Ambulance {ambulance.vehicle_no} is not available.')
                return redirect('ambulance_index')

            # Create trip
            trip = AmbulanceTrip.objects.create(
                patient=patient,
                ambulance=ambulance,
                start_time=start_time,
                booked_by=request.user
            )

            # Update ambulance status
            ambulance.status = 'busy'
            ambulance.save()

            messages.success(request, f'Ambulance trip created successfully for patient {patient.user.get_full_name()}.')
            return redirect('ambulance_index')

        except Exception as e:
            messages.error(request, f'Error creating trip: {str(e)}')
            return redirect('ambulance_index')

    return redirect('ambulance_index')
