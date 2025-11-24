from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from frontoffice.forms import PatientForm
from patient.models import Patient
from accounts.permissions import has_role


def home(request):
    return JsonResponse({"message": "FrontOffice Home"})


@login_required
def role_dashboard(request):
    role = getattr(request.user, 'role', None)
    role_name = role.name if role else 'Guest'
    return JsonResponse({"role": role_name})
    

# Receptionist patient list view
@login_required
def patient_list(request):
    if not has_role(request.user, 'Receptionist'):
        return JsonResponse(
            {"error": "Access denied: Only Receptionists can view patient list."},
            status=403
        )

    patients = Patient.objects.select_related('user').all()

    data = []
    for p in patients:
        data.append({
            "id": p.id,
            "name": f"{p.first_name} {p.last_name}",
            "phone": p.phone_number,
            "gender": p.gender,
            "dob": str(p.date_of_birth),
            "patient_id_hospital": p.patient_id_hospital,
        })

    return JsonResponse({"patients": data}, safe=False)


# receptionist create patient view
@login_required
def patient_create(request):
    if not has_role(request.user, 'Receptionist'):
        return JsonResponse(
            {"error": "Access denied: Only Receptionists can create patient records."},
            status=403
        )

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return JsonResponse(
                {"message": "Patient created successfully", "patient_id": patient.id}
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


# receptionist edit patient view
@login_required
def patient_edit(request, pk):
    if not has_role(request.user, 'Receptionist'):
        return JsonResponse(
            {"error": "Access denied: Only Receptionists can edit patient records."},
            status=403
        )

    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            return JsonResponse(
                {"message": "Patient updated successfully", "patient_id": patient.id}
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
